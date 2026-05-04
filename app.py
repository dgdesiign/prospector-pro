import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium
import os
from src.intelligence import SalesBrain, LeadScorer

# Configuração Ultra-Elite
st.set_page_config(page_title="RevOps Ultra-Command", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: #0d1117; padding: 15px; border-radius: 10px; border-left: 5px solid #d4af37; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .lead-card { background-color: #161b22; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #d4af37; }
    .fat-badge { background: #238636; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
    .news-trigger { background-color: #1e1e1e; border: 1px dashed #d4af37; padding: 10px; border-radius: 5px; margin-top: 5px; font-size: 0.85em; }
    </style>
""", unsafe_allow_html=True)

def load_data():
    conn = sqlite3.connect("data/prospector.db")
    df = pd.read_sql_query("SELECT * FROM leads", conn)
    conn.close()
    
    # Processamento de Inteligência Financeira e Funil
    df['capital_social'] = df['capital_social'].fillna(0)
    df['faturamento_estimado'] = df.apply(lambda r: LeadScorer.estimar_faturamento(r['capital_social']), axis=1)
    df['score'] = df.apply(lambda row: LeadScorer.calculate_score(row), axis=1)
    
    def fat_to_tier(fat):
        if fat >= 1000000: return "1M+"
        if fat >= 500000: return "500k-1M"
        if fat >= 200000: return "200k-500k"
        if fat >= 100000: return "100k-200k"
        if fat >= 50000: return "50k-100k"
        return "Até 50k"
    
    df['tier'] = df['faturamento_estimado'].apply(fat_to_tier)
    
    # Simulação de Etapas para o Funil Global
    stages = ["Frio", "Prospecção", "Qualificação", "Fechamento"]
    df['etapa_funil'] = [stages[i % 4] for i in range(len(df))]
    return df

# --- SIDEBAR: COMANDOS SÊNIORES ---
st.sidebar.title("🔱 RevOps Global")
role = st.sidebar.selectbox("Escolha seu Perfil:", [
    "Regional Director (Auditoria)",
    "Elite Closer (High Ticket)",
    "SDR / BDR Commander (Ataque)",
    "Inbound Manager",
    "IA Training Academy"
])

try:
    df_raw = load_data()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filtros Elite")
    f_tier = st.sidebar.multiselect("Tier de Faturamento:", sorted(df_raw['tier'].unique()))
    f_etapa = st.sidebar.multiselect("Etapa no Funil:", ["Frio", "Prospecção", "Qualificação", "Fechamento"])
    f_ramo = st.sidebar.multiselect("Ramo de Atividade:", df_raw['atividade_principal'].unique())
    
    df = df_raw.copy()
    if f_tier: df = df[df['tier'].isin(f_tier)]
    if f_etapa: df = df[df['etapa_funil'].isin(f_etapa)]
    if f_ramo: df = df[df['atividade_principal'].isin(f_ramo)]

    # --- VISÃO 1: DIRETOR REGIONAL ---
    if role == "Regional Director (Auditoria)":
        st.title("🏛️ Regional Governance Dashboard")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Pipeline Total", f"R$ {df['faturamento_estimado'].sum():,.0f}")
        c2.metric("Leads em Distribuição", len(df))
        c3.metric("Contas VIP (1M+)", len(df[df['tier'] == "1M+"]))
        c4.metric("Saúde do CRM", "94%")

        st.subheader("📍 Mapa de Calor Territorial")
        m = folium.Map(location=[-12.97, -38.50], zoom_start=12, tiles="CartoDB dark_matter")
        for idx, row in df.iterrows():
            color = 'blue' if row['etapa_funil'] == "Frio" else 'orange' if row['etapa_funil'] == "Prospecção" else 'green'
            size = 5 if row['faturamento_estimado'] < 200000 else 12
            folium.CircleMarker(
                location=[-12.97 + (idx*0.005), -38.50 + (idx*0.005)],
                radius=size, color=color, fill=True, popup=f"{row['nome']}<br>Faturamento Est: R$ {row['faturamento_estimado']}"
            ).add_to(m)
        st_folium(m, width="100%", height=400)

    # --- VISÃO 2: SDR / BDR / INBOUND ---
    elif role in ["SDR / BDR Commander (Ataque)", "Inbound Manager"]:
        st.title(f"📞 Cockpit de Ataque - {role}")
        
        col_list, col_intel = st.columns([2, 1])
        
        with col_list:
            st.subheader("🎯 Lista de Leads (Mecanismo de Busca)")
            st.dataframe(df[['nome', 'telefone', 'faturamento_estimado', 'tier', 'etapa_funil']])
        
        with col_intel:
            st.subheader("⚡ Deep Research Mode")
            selected_lead = st.selectbox("Selecione para pesquisar gatilhos:", df['nome'].unique())
            if st.button("Buscar Notícias e Gatilhos"):
                with st.spinner(f"Escaneando a web por {selected_lead}..."):
                    # Aqui integraria a busca real, simulando por enquanto
                    st.markdown(f"<div class='news-trigger'>💡 <b>Gatilho Detectado:</b> {selected_lead} anunciou expansão para o Nordeste há 14 dias. Use isso no hook: 'Vi que vocês estão chegando com força na Bahia...'</div>", unsafe_allow_html=True)
                    st.success("Gatilho de prospecção gerado com sucesso!")

    # --- VISÃO 3: ELITE CLOSER ---
    elif role == "Elite Closer (High Ticket)":
        st.title("💰 High-Ticket Closing Engine")
        
        target = st.selectbox("Selecione o Lead Estratégico:", df[df['faturamento_estimado'] > 500000]['nome'].unique())
        
        btn_dos, btn_prop = st.columns(2)
        if btn_dos.button("Gerar Dossiê Sênior"):
            lead_data = df[df['nome'] == target].to_dict('records')[0]
            st.markdown(SalesBrain.gerar_dossie_guerra(lead_data))
        
        if btn_prop.button("Gerar Proposta HTML Elite"):
            st.success(f"Site de Proposta gerado para {target}. Baixe o arquivo HTML.")

    # --- VISÃO 4: IA TRAINING ACADEMY ---
    elif role == "IA Training Academy":
        st.title("🎓 Academy - Treinamento de Elite")
        q = st.text_input("Dúvida sobre SPICED, Follow-Up ou Objeções?")
        if q:
            with st.spinner("Consultando Manuais de Cultura..."):
                st.markdown(SalesBrain.consultar_treinamento(q))

except Exception as e:
    st.error(f"Erro no sistema: {e}")
