from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

# Replace 'path/to/your/service-account-key.json' with the path to your service account key JSON file
SERVICE_ACCOUNT_FILE = 'tokenSA.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

# The email address of your regular Google account
REGULAR_ACCOUNT_EMAIL = 'yourmail@gmail.com.br'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Drive API service
service = build('drive', 'v3', credentials=credentials)

def create_folder(folder_name):
    # Define folder metadata
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        # 'writersCanShare': False
    }

    # Create the folder
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    
    print('Folder ID:', folder.get('id'))
    return folder.get('id')

def create_drive_file(folder_id):
    # Define file metadata
    file_metadata = {
        'name': 'MyFile.txt',  # Name of the file you want to create
        'parents': [folder_id],  # ID of the parent folder
        'mimeType': 'text/plain'  # MIME type of the file
    }

    # Content of the file
    content = 'Hello, World!'

    # Create the file
    media_body = MediaIoBaseUpload(BytesIO(content.encode()), mimetype='text/plain', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media_body, fields='id').execute()
    
    print('File ID:', file.get('id'))

    return file.get('id')

def list_files_and_folders():
    # List all files and folders
    results = service.files().list(fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])

    if not items:
        print('No files or folders found.')
    else:
        # return items
        print('Files and folders:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def share_access(file_id, email, role='reader'):
    if(role != 'reader' and role != 'writer' and role != 'owner'):
        raise ValueError('Invalid role. The role must be "reader" or "writer".')
    
    # if '@baidu' not in email:
    #     print("Não é possível compartilhar\nEste endereço de e-mail está vinculado a uma Conta do Google pessoal. O domínio Your Domain não permite o compartilhamento com contas pessoais.")
    #     return
    
    permissions = {
        'type': 'user',
        'role': role,
        'emailAddress': email
    }

    # Share access to the file or folder with the specified email address
    service.permissions().create(
        fileId=file_id,
        body=permissions,
        fields='id'
    ).execute()
    print('Access shared with', email)

def delete_drive_file(file_id):
    # Delete the file
    service.files().delete(fileId=file_id).execute()
    print('File deleted successfully.')


if __name__ == '__main__':
    # folder_id = create_folder('MyFolder')
    # file_id = create_drive_file(folder_id)
    files = list_files_and_folders()
    # print('Files and folders:')
    # for item in files:
    #     delete_drive_file(item['id'])

    # share_access(folder_id, REGULAR_ACCOUNT_EMAIL, 'writer')
    # delete_drive_file(id)
