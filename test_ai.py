import asyncio
from src.intelligence import LeadIntelligence

async def test_ai():
    print("🤖 Iniciando teste de Inteligência de Leads...")
    intel = LeadIntelligence()
    
    # Simulação de um lead real (Exemplo: Empresa de Energia Solar em Salvador)
    company = "Solar Tech Bahia"
    niche = "Instalação de Painéis Fotovoltaicos para Indústrias"
    
    print(f"🔍 Analisando Lead: {company} ({niche})")
    analysis = await intel.analyze_lead(company, niche)
    
    print("\n--- ESTRATÉGIA GERADA PELA IA ---")
    print(analysis)
    print("---------------------------------")

if __name__ == "__main__":
    asyncio.run(test_ai())
