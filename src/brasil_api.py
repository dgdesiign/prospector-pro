import httpx
import logging
import re

logger = logging.getLogger(__name__)

# Lista negra de termos que indicam que o email/telefone pode ser de contabilidade
CONTABILIDADE_KEYWORDS = [
    "contabil", "contabilidade", "escritorio", "assessoria", "tax", "auditoria",
    "contato@", "info@", "adm@", "administrativo"
]

async def consultar_cnpj_detalhado(cnpj: str):
    """
    Busca dados na Brasil API e aplica inteligência para separar 
    dados da empresa de dados da contabilidade.
    """
    cnpj_clean = re.sub(r'\D', '', cnpj)
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_clean}"
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=15.0)
            if resp.status_code != 200:
                return None
            
            data = resp.json()
            
            # Analisar se o email parece ser da contabilidade
            email_bruto = data.get("email", "") or ""
            is_accounting_email = any(word in email_bruto.lower() for word in CONTABILIDADE_KEYWORDS)
            
            # Formatar Quadro de Sócios (Tomadores de Decisão)
            socios = []
            for socio in data.get("qsa", []):
                socios.append({
                    "nome": socio.get("nome_socio"),
                    "cargo": socio.get("qualificacao_socio"),
                    "entrada": socio.get("data_entrada_sociedade")
                })

            return {
                "razao_social": data.get("razao_social"),
                "nome_fantasia": data.get("nome_fantasia"),
                "cnpj": data.get("cnpj"),
                "situacao": data.get("descricao_situacao_cadastral"),
                "data_abertura": data.get("data_inicio_atividade"),
                "capital_social": data.get("capital_social"),
                "email_oficial": email_bruto if not is_accounting_email else None,
                "email_contabilidade": email_bruto if is_accounting_email else None,
                "telefone": f"({data.get('ddd_telefone_1', '')[:2]}) {data.get('ddd_telefone_1', '')[2:]}",
                "endereco": f"{data.get('logradouro')}, {data.get('numero')} - {data.get('municipio')}/{data.get('uf')}",
                "socios": socios,
                "atividade_principal": data.get("cnae_fiscal_descricao"),
                "is_matriz": data.get("identificador_matriz_filial") == 1
            }
        except Exception as e:
            logger.error(f"Erro na investigação do CNPJ {cnpj}: {e}")
            return None
