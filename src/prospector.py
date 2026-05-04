import asyncio
import re
from src.google_maps import search_places, get_place_details
from src.models import Lead
from src.database import SessionLocal

def extract_phone(text):
    return re.sub(r'\s+', '', text) if text else None

def classify_tier(rating, total):
    if rating >= 4.5 and total >= 50:
        return "A"
    elif rating >= 4.0 and total >= 20:
        return "B"
    else:
        return "C"

async def fetch_leads(query, location=None, max_results=30):
    print(f"Buscando '{query}'...")
    places = await search_places(query, location, max_results=max_results)
    print(f"Encontrados {len(places)} locais.")
    leads = []
    sem = asyncio.Semaphore(5)
    
    async def process(place):
        async with sem:
            # Sênior: Se for mock, usa os dados do próprio objeto place
            if str(place.get("place_id", "")).startswith("mock_"):
                d = place
            else:
                d = await get_place_details(place["place_id"])
            
            name = d.get("name") or place.get("name", "Sem nome")
            phone = extract_phone(d.get("formatted_phone_number", ""))
            rating = d.get("rating", 0) or 0
            total = d.get("user_ratings_total", 0) or 0
            lead = {
                "nome": name, 
                "endereco": d.get("formatted_address", ""),
                "telefone": phone, 
                "site": d.get("website", ""),
                "rating": rating, 
                "user_ratings_total": total,
                "price_level": d.get("price_level", -1),
                "cnpj": None, 
                "razao_social": None,
                "atividade_principal": None, 
                "email": None,
                "tier": classify_tier(rating, total)
            }
            leads.append(lead)
            print(f"  {name} ⭐{rating} ({total})")
            
    await asyncio.gather(*[process(p) for p in places])
    leads.sort(key=lambda x: ({"A":0,"B":1,"C":2}[x["tier"]], -x["rating"]))
    return leads

def save_leads(leads):
    db = SessionLocal()
    for ld in leads:
        # Verifica se já existe pelo telefone
        exists = db.query(Lead).filter_by(telefone=ld["telefone"]).first() if ld["telefone"] else None
        if not exists:
            db.add(Lead(**ld))
    db.commit()
    db.close()
