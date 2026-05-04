# Projeto Prospector Pro - Diretrizes Sênior

## Stack Tecnológica
- **IA:** Gemini 1.5 Flash (Estável) / Gemini 2.5 Pro (Otimização)
- **Banco de Dados:** SQLite (Prospecção + Scraper Jurídico)
- **Frameworks:** `rich` (CLI), `sqlalchemy` (ORM), `playwright` (Scraper)

## Inteligência SalesBrain (Novo)
A `SalesBrain` é o motor de fechamento de alto ticket do sistema. Ela integra dados da Receita Federal com o banco de dados de processos jurídicos.

### Funcionalidades Principais:
1.  **Dossiê de Guerra:** Gera análise de poder, vulnerabilidade e perguntas SPICED para decisores.
2.  **Master Blueprint RevOps:** Cria planos estratégicos de faturamento e cronogramas de 90 dias.
3.  **Proposta Premium:** Gera sites HTML/CSS em Dark Mode para apresentações.
4.  **Integração Jurídica:** Cruza o CNPJ do lead com o banco `tribunal_data.db` do Scraper.

## Frameworks de Vendas Aplicados
- **SPICED:** (Situation, Pain, Impact, Critical Event, Decision). Foco total no **Impacto Financeiro**.
- **Value-Based Selling:** Ancoragem de preço baseada no patrimônio protegido ou lucro gerado.

## Comandos Operacionais
- **Busca de Leads:** `python src/cli.py` (Opção 1)
- **Investigação Sênior (CNPJ):** `python src/cli.py` (Opção 2)
- **Geração de Blueprint:** `python src/cli.py` (Opção 6)

## Segurança & Governança
- Chaves de API SEMPRE no `.env`.
- Auditoria de leads disponível via `cli.py` (Opção 5).
