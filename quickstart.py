from __future__ import print_function
import pickle
import os.path
import io
import glob
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']  # grabbing more privs than in the quickstart so I can screw with files down the line. 


def upload_docx(filename, service):
    file_metadata = {'name': filename,
                     'mimeType': 'application/vnd.google-apps.document'}
    media = MediaFileUpload(filename,
                            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    id = file.get('id')
    print("file id: " + id)
    return id


def download_pdf(file_id, filename, service):
    request = service.files().export_media(fileId=file_id,
                                           mimeType='application/pdf')
    fh = io.FileIO(filename, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Downloading: " + str(status.progress() * 100))
    # delete original file so as to not clutter up drive
    service.files().delete(fileId=file_id).execute()


def resolve_path(in_path):
    if in_path[0] == "~":
        return os.path.normpath(os.path.expanduser(in_path)) + "/"
    return os.path.abspath(in_path) + "/"


def get_globs(path, extension):
    st = resolve_path(path) + "*." + extension
    print(st)
    return glob.glob(st)


def convert_all_docs(service):
    if len(sys.argv) == 1:
        docs = glob.glob("*.docx")
    else:
        target_dir = sys.argv[1]
        docs = get_globs(target_dir, "docx")
    for filename in docs:
        file_id = upload_docx(filename, service)
        newfile = os.path.splitext(filename)[0] + ".pdf"
        download_pdf(file_id, newfile, service)


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # upload my test file:
    # fileid = upload_docx("testgdr.docx", service)
    # download_pdf(fileid, service)
    convert_all_docs(service)


if __name__ == '__main__':
    main()
