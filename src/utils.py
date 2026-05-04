import httpx

async def fetch_cnpj_data(cnpj: str):
    cnpj_clean = "".join(filter(str.isdigit, cnpj))
    if len(cnpj_clean) != 14:
        return {}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_clean}", timeout=10.0)
            return resp.json() if resp.status_code == 200 else {}
        except Exception:
            return {}
