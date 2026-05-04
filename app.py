import streamlit as st
import pandas as pd
import sqlite3
import asyncio
from src.intelligence import LeadIntelligence

# Configuração da Página
st.set_page_config(page_title="Prospector Pro Dashboard", page_icon="📈", layout="wide")

st.title("🚀 Prospector Pro - Lead Intelligence")
st.markdown("---")

# Sidebar para Filtros e Configurações
st.sidebar.header("Configurações")
db_path = "data/prospector.db"

# Função para carregar dados
def load_data():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM leads", conn)
    conn.close()
    return df

try:
    df = load_data()
    
    # KPIs no topo
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Leads", len(df))
    col2.metric("Niches Identificados", len(df['nicho'].unique()))
    col3.metric("Status", "Online")

    st.subheader("📋 Lista de Leads Qualificados")
    
    # Filtro de busca
    search = st.text_input("Buscar empresa ou nicho:")
    if search:
        df = df[df['nome'].str.contains(search, case=False) | df['nicho'].str.contains(search, case=False)]

    st.dataframe(df, use_container_width=True)

    # Seção de Inteligência Artificial
    st.markdown("---")
    st.subheader("🤖 IA Sales Strategist")
    
    selected_company = st.selectbox("Selecione um lead para análise estratégica:", df['nome'].unique())
    
    if st.button("Gerar Estratégia de Venda"):
        lead_info = df[df['nome'] == selected_company].iloc[0]
        intel = LeadIntelligence()
        
        with st.spinner(f'IA analisando {selected_company}...'):
            # Rodando o método assíncrono da IA
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            analysis = loop.run_until_complete(intel.analyze_lead(lead_info['nome'], lead_info['nicho']))
            
            st.success("Análise Concluída!")
            st.markdown(f"### 🎯 Estratégia para {selected_company}")
            st.info(analysis)

except Exception as e:
    st.error(f"Erro ao carregar banco de dados: {e}")
    st.info("Certifique-se de que o banco de dados 'data/prospector.db' existe e possui dados.")

