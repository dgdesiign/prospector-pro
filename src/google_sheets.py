import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

# Token que você forneceu
DRIVE_TOKEN = os.getenv("GOOGLE_DRIVE_TOKEN")

def get_sheets_service():
    """
    Sênior: Inicializa o serviço do Google Sheets.
    Pode usar Service Account ou Token direto.
    """
    try:
        if DRIVE_TOKEN and len(DRIVE_TOKEN) > 20:
            # Tenta usar o token fornecido diretamente
            creds = Credentials(DRIVE_TOKEN)
            return build('sheets', 'v4', credentials=creds)
        else:
            print("Aviso: Credenciais do Google Drive não configuradas corretamente.")
            return None
    except Exception as e:
        print(f"Erro ao conectar com Google Sheets: {e}")
        return None

async def export_leads_to_sheets(spreadsheet_id, range_name, leads):
    """Exporta uma lista de leads para uma planilha específica."""
    service = get_sheets_service()
    if not service:
        return False

    values = []
    for lead in leads:
        values.append([
            lead.get("nome"),
            lead.get("telefone"),
            lead.get("cnpj"),
            lead.get("tier"),
            lead.get("email_oficial")
        ])

    body = {'values': values}
    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        print(f"Sincronizado com Google Sheets: {result.get('updates').get('updatedCells')} células atualizadas.")
        return True
    except HttpError as error:
        print(f"Erro na API do Google Sheets: {error}")
        return False
