from __future__ import print_function
import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
CLIENT_CREDS = "../auth/email/client_creds.json"
ACCESS_TOKEN = "../auth/email/access_token.json"

def send_email():
    """Send email"""
    creds = None
    if os.path.exists(ACCESS_TOKEN):
        creds = Credentials.from_authorized_user_file(ACCESS_TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_CREDS, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(ACCESS_TOKEN, "w") as token:
            token.write(creds.to_json())
    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()
        message["From"] = "lalit.c@ahduni.edu.in"
        message["To"] = [
            "lalitshankarch@gmail.com",
        ]
        message["Subject"] = "Professorate"
        message.set_content(
            "Please fill the weekly form: https://forms.gle/A4WJ4EACGPWkAyvx9"
        )
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        service.users().messages().send(userId="me", body=create_message).execute()
        print("Email(s) successfully sent!")
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    send_email()