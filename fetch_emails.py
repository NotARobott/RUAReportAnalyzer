from googleapiclient.discovery import build
from authenticate_gmail import authenticate_gmail
from config import load_config
import base64

def fetch_dmarc_reports():
    config = load_config()
    query = config["gmail_search_filter"]
    
    service = build('gmail', 'v1', credentials=authenticate_gmail())
    messages = service.users().messages().list(userId='me', q=query).execute().get('messages', [])

    if not messages:
        print("No matching emails found.")
        return []

    attachments = []
    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        for part in message['payload'].get('parts', []):
            if part['filename'].endswith((".zip", ".gz")):
                
                attachment = service.users().messages().attachments().get(
                    userId='me', messageId=msg['id'], id=part['body']['attachmentId']).execute()
                file_data = base64.urlsafe_b64decode(attachment['data'])

                print(f"Downloaded and decoded attachment: {part['filename']} (size: {len(file_data)} bytes)")

                attachments.append(file_data)

                service.users().messages().delete(userId='me', id=msg['id']).execute()
                print(f"Deleted email with ID: {msg['id']}")
    
    return attachments
