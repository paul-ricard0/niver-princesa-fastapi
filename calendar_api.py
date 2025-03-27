from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os

CREDENTIALS_FILE = "credentials.json"  # Substitua pelo caminho correto
TOKEN_FILE = "token.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    """Autentica via OAuth 2.0"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    service = build("calendar", "v3", credentials=creds)
    return service

def create_evento_aniversario(service):
    # Definir o evento
    event = {
        "summary": "🎉 Aniversário da Fabrícia! 🎂🎈",
        "location": "Rua Coração Eucarístico de Jesus, 180 - Coração Eucarístico, Belo Horizonte - MG, 30535-460, Brasil",
        "description": '''
        🎉 Aniversário da Fabrícia! 🎂🎈\n
        Oi, pessoal! Estou super animado para comemorar mais um ano de vida com vocês! 🥳 \n
        Vamos nos reunir no Taco's Bar e Espetaria para uma noite de diversão, boa comida e ótimos momentos.
        📍 Local: Taco's Bar e Espetaria\n
        📅 Data: Sábado, 5 de abril de 2025\n
        ⏰ Horário: 20h00 às 00h15\n
        Conto com a presença de todos para tornar essa celebração ainda mais especial! 💛 Confirme sua presença e nos vemos lá! 🎊🍻
        ''',
        "start": {
            "dateTime": "2025-04-05T20:00:00-03:00",
            "timeZone": "America/Sao_Paulo",
        },
        "end": {
            "dateTime": "2025-04-06T00:15:00-03:00",
            "timeZone": "America/Sao_Paulo",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 30},  # Lembrete 30 min antes
                {"method": "email", "minutes": 1440},  # Lembrete 1 dia antes
            ],
        },
    }

    # Criar o evento no Google Calendar
    created_event = service.events().insert(calendarId="primary", body=event, conferenceDataVersion=1).execute()
    print(f"Evento criado: {created_event['htmlLink']}")
    return created_event["id"]

def listar_eventos(service):
    # Listar os próximos eventos do calendário principal
    calendar_id = "primary"  # Use um ID de calendário específico, se necessário
    events_result = service.events().list(
        calendarId=calendar_id, maxResults=10, singleEvents=True, orderBy="startTime"
    ).execute()

    # Exibir eventos
    events = events_result.get("items", [])
    if not events:
        print("Nenhum evento encontrado.")
    else:
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            event_id = event["id"]  # Pega o ID do evento
            print(f"{start} - {event['summary']} (ID: {event_id})")


def buscar_id_evento(service, nome_reuniao):
    events_result = service.events().list(
        calendarId="primary",
        q=nome_reuniao,  # Filtra eventos com esse nome
        # timeMin=f"{ano}-{mes}-{dia}T00:00:00Z",  # Busca a partir dessa data
        maxResults=5,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = events_result.get("items", [])
    if events:
        return events[0]["id"]  # Retorna o ID do primeiro evento encontrado
    return None  # Retorna None se não encontrar o evento
    

def excluir_evento(service, nome_reuniao):
    
    event_id = buscar_id_evento(service, nome_reuniao)
    # Verificar se o evento foi encontrado
    if event_id:
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print("Evento excluído com sucesso!")
    else:
        print("Evento não encontrado.")


def add_attendee(service, event_id, email):
    """Adiciona um único convidado ao evento existente"""
    
    event = service.events().get(calendarId="primary", eventId=event_id).execute()
    event["attendees"] = [{"email": email}]

    updated_event = service.events().update(calendarId="primary", eventId=event_id, body=event).execute()
    print(f"Convidado {email} adicionado com sucesso!")

# if __name__ == "__main__":
#     service = get_calendar_service()
#     event_id = '584ucrgkght9bsok4nr0bgog3b'
#     email = 'fabricia.agrimensura@gmail.com'
#     add_attendee(service, event_id, email) 
