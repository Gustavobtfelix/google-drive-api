from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

# Replace 'path/to/your/service-account-key.json' with the path to your service account key JSON file
SERVICE_ACCOUNT_FILE = 'token.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

# The email address of your regular Google account
REGULAR_ACCOUNT_EMAIL = 'yourmail@gmail.com.br'

def create_drive_file():
    # Authenticate using the service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    # Build the Google Drive API service
    service = build('drive', 'v3', credentials=credentials)
    
    # Define file metadata
    file_metadata = {
        'name': 'MyFile.txt',  # Name of the file you want to create
        'mimeType': 'text/plain'  # MIME type of the file
    }

    # Content of the file
    content = 'Hello, World!'

    # Create the file
    media_body = MediaIoBaseUpload(BytesIO(content.encode()), mimetype='text/plain', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media_body, fields='id').execute()
    
    print('File ID:', file.get('id'))

    # Share the file with your regular Google account
    service.permissions().create(fileId=file.get('id'), body={'type': 'user', 'role': 'writer', 'emailAddress': REGULAR_ACCOUNT_EMAIL}).execute()
    print('File shared with', REGULAR_ACCOUNT_EMAIL)

if __name__ == '__main__':
    create_drive_file()
