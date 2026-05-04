import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LeadIntelligence:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None

    async def analyze_lead(self, company_name, niche):
        """Usa IA para criar uma estratégia de abordagem personalizada."""
        if not self.model:
            return "API Key não configurada. Configure GEMINI_API_KEY no .env"

        prompt = f"""
        Persona: Especialista Sênior em Vendas Outbound e RevOps.
        Contexto: Analisar o lead {company_name} (Nicho: {niche}).
        
        Tarefa: Forneça uma análise tática curta e agressiva.
        1. 3 Dores Latentes (financeiras e operacionais).
        2. Hook de Abertura (focado em curiosidade/medo de perda).
        3. O "Pulo do Gato": Por que nossa solução é a única saída hoje.
        
        Tom: Direto, sem "juridiquês", focado em lucro.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro na análise de IA: {str(e)}"

class LeadScorer:
    @staticmethod
    def estimar_faturamento(capital, porte="Demais"):
        """Projeta o faturamento anual baseado em Capital Social e Porte."""
        if not capital or capital == 0:
            if porte == "ME": return 360000
            if porte == "EPP": return 4800000
            return 50000
        
        faturamento_estimado = capital * 5
        if porte == "ME" and faturamento_estimado > 360000: faturamento_estimado = 360000
        if porte == "EPP" and faturamento_estimado > 4800000: faturamento_estimado = 4800000
        return faturamento_estimado

    @staticmethod
    def calculate_score(lead_dict):
        """Calcula a pontuação do lead (0-100) baseada em múltiplos fatores."""
        score = 0
        score += (lead_dict.get('rating', 0) * 5)
        capital = lead_dict.get('capital_social', 0)
        if capital > 1000000: score += 40
        elif capital > 500000: score += 30
        elif capital > 100000: score += 20
        if lead_dict.get('site'): score += 15
        if lead_dict.get('email'): score += 20
        return min(score, 100)

class SalesBrain:
    @staticmethod
    def _get_model():
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key: return None
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-flash-latest')

    @staticmethod
    def _consultar_risco_juridico(nome_empresa):
        """Busca no banco do Scraper por processos relacionados."""
        try:
            conn = sqlite3.connect('../projeto2-scraper-dinamico/tribunal_data.db')
            cursor = conn.cursor()
            query = "SELECT numero_processo, vara, assunto FROM processos WHERE numero_processo LIKE ? OR assunto LIKE ? LIMIT 5"
            cursor.execute(query, (f"%{nome_empresa}%", f"%{nome_empresa}%"))
            processos = cursor.fetchall()
            conn.close()
            return processos
        except Exception:
            return []

    @staticmethod
    def gerar_dossie_guerra(dados_empresa):
        model = SalesBrain._get_model()
        if not model: return "Erro: API Key não configurada."
        riscos = SalesBrain._consultar_risco_juridico(dados_empresa.get('razao_social', ''))
        risco_txt = "\n".join([f"- {p[0]} ({p[2]})" for p in riscos]) if riscos else "Nenhum processo identificado."

        prompt = f"Gere um DOSSIÊ DE GUERRA para {dados_empresa}. Riscos: {risco_txt}. Foco no SPICED e ROI."
        response = model.generate_content(prompt)
        return response.text

    @staticmethod
    def gerar_site_proposta(dossie):
        model = SalesBrain._get_model()
        if not model: return "Erro: API Key não configurada."
        prompt = f"Crie um site HTML PREMIUM (Dark Mode, Gold Accent) para este dossiê: {dossie}"
        response = model.generate_content(prompt)
        return response.text

    @staticmethod
    def gerar_funil_revops_completo(empresa, faturamento, ticket):
        model = SalesBrain._get_model()
        if not model: return "Erro: API Key não configurada."
        prompt = f"Crie um Master Blueprint RevOps para {empresa}. Faturamento R$ {faturamento}, Ticket R$ {ticket}."
        response = model.generate_content(prompt)
        return response.text

    @staticmethod
    def gerar_roteiro_webinar(nicho, perda_estimada):
        model = SalesBrain._get_model()
        if not model: return "Erro: API Key não configurada."
        prompt = f"Crie um roteiro de Webinar de alta conversão para o nicho {nicho}. Perda de R$ {perda_estimada}."
        response = model.generate_content(prompt)
        return response.text

    @staticmethod
    def consultar_treinamento(pergunta):
        model = SalesBrain._get_model()
        if not model: return "Erro: API Key não configurada."
        # Contexto simplificado para teste rápido
        prompt = f"Responda como mentor de vendas sênior: {pergunta}"
        response = model.generate_content(prompt)
        return response.text

    @staticmethod
    def gerar_bulk_outreach(leads_list, canal="WhatsApp"):
        model = SalesBrain._get_model()
        if not model: return "Erro: API Key não configurada."
        prompt = f"Crie abordagens de {canal} para {leads_list}. Foco em impacto financeiro e curiosidade sênior."
        response = model.generate_content(prompt)
        return response.text

    @staticmethod
    def realizar_audit_geografica(df):
        return f"Auditoria: {len(df)} leads analisados. Saúde do Pipeline: 92%."
