# 🚀 Prospector Pro - Inteligência em Vendas

O **Prospector Pro** é um motor de busca e enriquecimento de leads desenvolvido para automatizar a descoberta de oportunidades de negócio altamente qualificadas.

## 🛠️ Tecnologias
- **Python 3.12**
- **SQLite** para armazenamento local
- **Google Maps API** (Geolocalização de empresas)
- **Brasil API** (Enriquecimento de dados de CNPJ)
- **Google Sheets API** (Exportação direta para planilhas)

## 🎯 Funcionalidades
- **Busca por Nicho:** Encontra empresas por localização e setor usando Google Maps.
- **Enriquecimento de CNPJ:** Consulta automática de sócios, capital social e situação cadastral.
- **Scoring de Leads:** Algoritmo para classificar leads com maior potencial de conversão.
- **Exportação:** Sincronização automática com Google Sheets e exportação em CSV.

## 📁 Estrutura do Projeto
- `src/prospector.py`: Core logic da busca.
- `src/intelligence.py`: Lógica de qualificação e scoring.
- `src/google_maps.py`: Integração com Place API.
- `src/brasil_api.py`: Consulta de dados governamentais.

