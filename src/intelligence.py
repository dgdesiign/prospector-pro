import re

class SalesBrain:
    """
    Motor de Inteligência v11.0 - REVOPS SCALER.
    Unifica a Escavação de Dados (CNPJ/MAPS) com o Framework SPICED.
    """

    @classmethod
    def calcular_perda_estimada(cls, dados_lead):
        """
        Calcula o 'Impacto' (I do SPICED). 
        Quanto dinheiro o lead perde por ser invisível ou ter má reputação.
        """
        reviews = dados_lead.get("user_ratings_total", 0)
        rating = dados_lead.get("rating", 0)
        capital = dados_lead.get("capital_social", 0) or 50000 # Default para pequenos
        
        # Faturamento Estimado Mensal (Baseado em Capital Social)
        faturamento_est = (capital * 0.2) / 12 
        
        perda_por_demanda = 0
        if reviews < 30:
            # Perde 40% do potencial de mercado por não ser encontrado
            perda_por_demanda = faturamento_est * 0.4
        
        perda_por_oferta = 0
        if 0 < rating < 4.3:
            # Perde 30% das vendas por má reputação/avaliação
            perda_por_oferta = faturamento_est * 0.3
            
        return perda_por_demanda + perda_por_oferta

    @classmethod
    def gerar_dossie_guerra(cls, dados_lead):
        """
        Gera o Dossiê Completo que será o entregável de alto valor.
        """
        perda = cls.calcular_perda_estimada(dados_lead)
        capital = dados_lead.get("capital_social", 0) or 0
        socios = dados_lead.get("socios", [])
        decisor_principal = socios[0]['nome'] if socios else "O Responsável"
        
        # Lógica de Gancho CAA (Cadência de Abordagem Ativa)
        gancho = ""
        if reviews := dados_lead.get("user_ratings_total", 0) < 15:
            gancho = f"Notei que a {dados_lead['nome']} é invisível no Google comparada ao seu capital de R$ {capital:,.2f}."
        elif dados_lead.get("rating", 0) < 4.2:
            gancho = f"Vi que a reputação digital da {dados_lead['nome']} está drenando o lucro que vocês deveriam ter."
        else:
            gancho = f"Mapeei o fluxo de decisores da {dados_lead['nome']} e vi que falta o motor de tração BUILD."

        return {
            "identificacao": {
                "nome": dados_lead.get("nome"),
                "cnpj": dados_lead.get("cnpj"),
                "capital": f"R$ {capital:,.2f}",
                "decisores": [s['nome'] for s in socios]
            },
            "diagnostico_spiced": {
                "S_Situação": "Empresa estabelecida mas com GAP de autoridade digital.",
                "P_Dor": "Dependência de indicação e alto custo de oportunidade.",
                "I_Impacto": f"Perda estimada de R$ {perda:,.2f} por mês.",
                "C_Evento_Critico": "Saturação do mercado local nos próximos 60 dias.",
                "D_Decisao": f"{decisor_principal} (Sócio-Administrador)"
            },
            "script_caa_d1": (
                f"Olá {decisor_principal}, aqui é [Seu Nome]. "
                f"Liguei porque identifiquei que a {dados_lead['nome']} está deixando cerca de R$ {perda:,.2f} "
                "na mesa todos os meses por um gargalo específico na sua [Demanda/Conversão]. "
                "Podemos estancar esse sangue em 15 minutos amanhã?"
            )
        }

    @classmethod
    def calcular_projeto(cls, perda_mensal):
        """Define preço e tempo com base no Impacto Financeiro."""
        # Preço é 25% da perda anual estimada ou 3x a perda mensal (o que for maior)
        preco_sugerido = max(perda_mensal * 3, 5000)
        tempo_semanas = 4 if preco_sugerido < 15000 else 8
        return preco_sugerido, tempo_semanas

    @classmethod
    def gerar_site_proposta(cls, dossie):
        """Gera um HTML de altíssimo valor percebido para a proposta."""
        id_info = dossie['identificacao']
        spiced = dossie['diagnostico_spiced']
        
        # Sênior: Extração robusta de valor numérico para evitar erros de conversão
        import re
        impacto_str = spiced['I_Impacto']
        match = re.search(r'[\d.,]+', impacto_str.replace('.', '').replace(',', '.'))
        perda_valor = float(match.group()) if match else 500.0
        
        preco, tempo = cls.calcular_projeto(perda_valor)

        html_template = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Proposta Estratégica - {id_info['nome']}</title>
            <style>
                body {{ font-family: 'Inter', sans-serif; background: #0a0a0a; color: #fff; line-height: 1.6; margin: 0; padding: 40px; }}
                .container {{ max-width: 900px; margin: auto; border: 1px solid #333; padding: 40px; border-radius: 20px; background: #111; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }}
                h1 {{ color: #00ff88; font-size: 42px; margin-bottom: 10px; }}
                .highlight {{ color: #ff3366; font-weight: bold; font-size: 24px; }}
                .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }}
                .card {{ background: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 4px solid #00ff88; }}
                .impact-card {{ border-left-color: #ff3366; background: rgba(255, 51, 102, 0.05); }}
                .btn {{ display: inline-block; padding: 15px 30px; background: #00ff88; color: #000; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 30px; }}
                .timeline {{ margin-top: 40px; border-top: 1px solid #333; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <p style="text-transform: uppercase; letter-spacing: 2px; color: #666;">Dossiê de Inteligência RevOps</p>
                <h1>{id_info['nome']}</h1>
                <p>Diagnóstico elaborado para <strong>{spiced['D_Decisao']}</strong></p>

                <div class="grid">
                    <div class="card">
                        <h3>🔍 Cenário Atual</h3>
                        <p>{spiced['S_Situação']}</p>
                    </div>
                    <div class="card impact-card">
                        <h3>🚨 Vazamento de Receita</h3>
                        <p class="highlight">{spiced['I_Impacto']}</p>
                        <p>Prejuízo mensal estimado por falha de processo.</p>
                    </div>
                </div>

                <div class="timeline">
                    <h2>🗺️ Plano de Guerra (Implementação {tempo} semanas)</h2>
                    <p><strong>Fase 1 (TEACH):</strong> Auditoria profunda e correção de gânglios expostos.</p>
                    <p><strong>Fase 2 (BUILD):</strong> Construção da Máquina de Prospecção Ativa (CAA).</p>
                    <p><strong>Fase 3 (MANAGE):</strong> Treinamento do time e monitoramento de KPIs.</p>
                </div>

                <div style="text-align: center; margin-top: 50px;">
                    <p>Investimento para Estancamento e Reversão:</p>
                    <div style="font-size: 48px; font-weight: bold;">R$ {preco:,.2f}</div>
                    <a href="#" class="btn">ACEITAR IMPLEMENTAÇÃO E COMEÇAR AMANHÃ</a>
                </div>
            </div>
        </body>
        </html>
        """
        return html_template

    @classmethod
    def gerar_roteiro_webinar(cls, nicho, nivel_oferta="36k"):
        """Gera roteiros segmentados por nível de ticket (Escada de Valor)."""
        ofertas = {
            "500": {"nome": "Diagnóstico Raio-X", "entrega": "Dossiê de Perda Financeira + Auditoria Digital"},
            "3k": {"nome": "Cadência Ativa", "entrega": "Playbook Comercial + Scripts CAA + GMN"},
            "15k": {"nome": "Máquina 1.0", "entrega": "CRM + VoIP + Treinamento Modo Caverna"},
            "36k": {"nome": "RevOps Full", "entrega": "Infra Completa + IA de Vendas + Onboarding 28 dias"},
            "77k": {"nome": "Mastermind CEO", "entrega": "Squad RevOps + Mentoria Estratégica + Ecossistema IA"}
        }
        
        info = ofertas.get(nivel_oferta, ofertas["36k"])
        
        md = f"""# 🎥 Webinar de Escala: Estratégia {nivel_oferta} para {nicho}
        
## ⚡ GANCHO DE AUTORIDADE
"Nós escavamos o mercado de {nicho} e encontramos um padrão: empresas estão perdendo até 40% do faturamento por falta de processos. Hoje vamos mostrar como implementar o {info['nome']}."

## 🛠️ O QUE VOCÊ VAI RECEBER
- **{info['entrega']}**

## 💰 A OFERTA IRRECUSÁVEL
"A implementação normal custaria R$ {nivel_oferta}. Mas para quem está aqui, vamos liberar o Diagnóstico de R$ 500 com garantia total. Se não acharmos vazamento, não pagará nada."
"""
        return md

    @classmethod
    def gerar_landing_page_webinar(cls, nicho, nivel_oferta):
        """Gera uma Landing Page de alta conversão para o Webinar."""
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Workshop Exclusivo: {nicho} High-Performance</title>
            <style>
                body {{ font-family: 'Inter', sans-serif; background: #000; color: #fff; text-align: center; padding: 50px; }}
                .box {{ max-width: 700px; margin: auto; background: #111; padding: 40px; border: 1px solid #00ff88; border-radius: 15px; }}
                h1 {{ color: #00ff88; font-size: 36px; }}
                .warning {{ color: #ff3366; font-size: 20px; font-weight: bold; margin: 20px 0; }}
                .btn {{ display: block; padding: 20px; background: #00ff88; color: #000; font-weight: bold; text-decoration: none; border-radius: 10px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="box">
                <p>EVENTO ONLINE E GRATUITO</p>
                <h1>O Fim do Vazamento de Lucro em {nicho}</h1>
                <div class="warning">Descobrimos como empresas da sua região estão perdendo até R$ 15.000,00 por mês.</div>
                <p>Nesta aula de 40 minutos, vamos abrir a caixa preta da Engenharia de Receita e mostrar como implementar o sistema de {nivel_oferta}.</p>
                <a href="#" class="btn">RESERVAR MINHA VAGA AGORA</a>
                <p style="font-size: 12px; margin-top: 20px;">Restam apenas 12 vagas para este workshop.</p>
            </div>
        </body>
        </html>
        """
        return html

    @classmethod
    def exportar_ranking_oportunidade(cls, leads_list):
        """Gera um CSV ordenado pelo Impacto Financeiro (perda estimada)."""
        import csv
        file_name = "ranking_oportunidade_revops.csv"
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['NOME', 'CIDADE', 'CAPITAL', 'RATING', 'PERDA_MENSAL_ESTIMADA', 'TIER_REVOPS'])

            for l in leads_list:
                perda = cls.calcular_perda_estimada(l)
                writer.writerow([
                    l.get('nome'), 
                    l.get('endereco', '').split(',')[-1].strip(),
                    l.get('capital_social', 0),
                    l.get('rating', 0),
                    f"{perda:.2f}",
                    l.get('tier', 'C')
                ])
        return file_name


    @classmethod
    def gerar_funil_revops_completo(cls, nome_empresa, faturamento_atual, ticket_medio):
        """O Produto Final de Alto Ticket: Integra Playbook, Follow-up e a Matemática do ROI."""
        # Matemática da Proposta (Baseado no Exemplo de 15k/36k)
        leads_estimados = 100
        conversao_atual = 0.05
        vendas_atuais = leads_estimados * conversao_atual
        
        conversao_projetada = 0.08
        vendas_projetadas = leads_estimados * conversao_projetada
        aumento_faturamento = (vendas_projetadas - vendas_atuais) * ticket_medio
        
        preco_projeto = 15000 if aumento_faturamento < 30000 else 36000

        md = f"""# 🚀 MASTER BLUEPRINT REVOPS: {nome_empresa}
*A Engenharia de Receita de Ponta a Ponta*

---

## 💰 1. A MATEMÁTICA DO ROI (A OFERTA IRRECUSÁVEL)
**Cenário Atual:**
* Faturamento Base: R$ {faturamento_atual:,.2f}
* Ticket Médio: R$ {ticket_medio:,.2f}
* Gargalo: Leads perdidos por falta de CRM e processo SPICED.

**Projeção Pós-Implementação:**
* Aumento de Conversão (de 5% para 8%).
* Retorno Adicional Mensal Projetado: **+ R$ {aumento_faturamento:,.2f}/mês**

**O Carrinho de R$ {preco_projeto:,.2f}:**
1. **Fase 1 (Sprints):** Raio-X, Playbook Comercial, Script SPICED.
2. **Fase 2 (Infra):** CRM, Dashboard de Gestão.
3. **Fase 3 (Operação):** Treinamento, Follow-up ativo e Roleplay.
*Argumento de Fechamento:* "Você me paga R$ {preco_projeto:,.2f} uma vez, para eu instalar uma máquina que te devolve R$ {aumento_faturamento:,.2f} TODOS OS MESES. Isso não é custo, é um ROI massivo."

---

## 🛡️ 2. PLAYBOOK DE ATAQUE (SDR)
* **Rotina Modo Caverna:** 09:00 às 11:30 (Foco Ouro), Celular Desligado, Gatilho do Perfume.
* **Filtro Pix/Serasa:** Ignorar empresas sem presença digital. Focar nas que têm capital mas não têm autoridade.
* **Abordagem de Choque:** *"Doutor, vou direto ao ponto. Se eu te mostrar como estancar um vazamento de lucro que a sua clínica tem hoje, você me dá 1 minuto?"*
* **Qualificação SPICED:** Investigar a [S]ituação, instigar a [P]ain, quantificar o [I]mpacto Financeiro, extrair o [C]ritical Event e alinhar com o [D]ecisor.

---

## 🔁 3. MANUAL DE FOLLOW-UP E NO-SHOW
Quem controla o processo, controla o fechamento. O lead nunca fica solto.
* **Na Ligação (Ancoragem):** "Vou reservar o dia X às Yh. Já te envio a confirmação no WhatsApp com o protocolo."
* **No WhatsApp (Imediato):** "Reserva Confirmada ✅ Protocolo #1501. O não comparecimento sem aviso prévio cancela a sua auditoria."
* **Dia da Reunião:** Enviar link 10 min antes. Se não confirmar, ligar.

---

## 📈 4. O DASHBOARD DO DONO (GESTÃO)
*O Fim da Intuição. O Início dos Dados.*
* **Nível 1:** A Auditoria (Ensino do Problema).
* **Nível 2:** A Construção (Playbook, Cadência, CRM).
* **Nível 3:** A Gestão (Painel de Controle).
O dono agora abre o celular às 9h e sabe exatamente quantos leads entraram, quantos SPICEDs foram feitos e qual a previsão de fechamento real.
"""
        return md



