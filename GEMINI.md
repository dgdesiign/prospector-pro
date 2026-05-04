# Projeto Prospector Pro - Diretrizes para o Gemini CLI

## Stack Tecnológica
- **Linguagem:** Python 3.12+
- **Banco de Dados:** SQLite (via SQLAlchemy)
- **Bibliotecas Principais:** `httpx`, `rich`, `python-dotenv`, `sqlalchemy`
- **Linting/Formatação:** `ruff`

## Convenções de Código
- **Estilo:** Seguir o padrão PEP 8.
- **Async:** Usar `asyncio` e `httpx.AsyncClient` para operações de rede.
- **SQLAlchemy:** Usar `SessionLocal` para operações de banco e garantir o fechamento da sessão.
- **Interface:** Manter a interface CLI amigável usando a biblioteca `rich`.

## Comandos Úteis
- **Linting:** `ruff check .`
- **Formatação:** `ruff format .`
- **Execução:** `python main.py`

## Segurança
- Nunca exibir chaves de API do Google Maps em logs ou no chat.
- Chaves devem estar sempre no arquivo `.env`.
