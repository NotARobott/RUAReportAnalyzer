import os
import base64
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from authenticate_gmail import authenticate_gmail

def gmail_send_email(subject, body, to_email, attachment_path):
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEMultipart()
    message['to'], message['subject'] = to_email, subject
    message.attach(MIMEText(body, 'plain'))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(f.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            message.attach(mime_base)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
    print(f"Email sent to {to_email}.")
