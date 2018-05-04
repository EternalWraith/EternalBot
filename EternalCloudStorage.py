import os, io

from apiclient.discovery import build
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('login.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

def getFileStore():
    f = open("store.txt","r")
    ff = f.read().split("\n")
    out = {}
    for i in ff:
        if i != "":
            inp = i.split(" ")
            out[inp[0]] = inp[1]
    return out

def setFileStore(filestorage):
    f = open("store.txt","w")
    t = ""
    for i in filestorage:
        t += "{0} {1}\n".format(i,filestorage[i])
    f.write(t)

def clearFileStore():
    f = open("store.txt","w")
    f.write("")
    
def upload(filename):
    metadata = {'name': filename}
    filestorage = getFileStore()
    #print(filestorage)
    if filename in filestorage:
        file_id = filestorage[filename]
        file = service.files().get(fileId=file_id).execute()
        media_body = MediaFileUpload(
        filename, mimetype='application/x-sqlite3', resumable=True)

        updated_file = service.files().update(
        fileId=file_id,
        #body=file,
        media_body=media_body).execute()
    else:
        media = MediaFileUpload(filename,
                            mimetype='application/x-sqlite3')
        file = service.files().create(body=metadata,
                                        media_body=media,
                                        fields='id').execute()
        filestorage[filename] = file["id"]
        setFileStore(filestorage)
    print('Uploaded "%s"' % (filename))

def download(file_name, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    print('Downloaded "%s" (%s)' % (file_name, file_id))
    contents = fh.getvalue()
    outf = open(file_name, "wb")
    outf.write(contents)
    outf.close()
    filestorage = getFileStore()
    filestorage[file_name] = file_id
    setFileStore(filestorage)

def download_all():
    clearFileStore()
    items = []
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items += results.get('files', [])
    token = results.get('nextPageToken', None)
    while token != None:
        results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items += results.get('files', [])
        token = results.get('nextPageToken', None)
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            download(item['name'], item['id'])
