import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LeadIntelligence:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    async def analyze_lead(self, company_name, niche):
        """Usa IA para criar uma estratégia de abordagem personalizada."""
        if not self.model:
            return "API Key não configurada. Configure GEMINI_API_KEY no .env"

        prompt = f"""
        Como um especialista em vendas outbound, analise este lead:
        Empresa: {company_name}
        Nicho: {niche}
        
        Forneça:
        1. 3 Pontos de dor prováveis.
        2. Uma frase de abertura (hook) para Cold Call.
        3. Um motivo único para eles contratarem nossos serviços agora.
        
        Seja direto, agressivo e profissional.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro na análise de IA: {str(e)}"

