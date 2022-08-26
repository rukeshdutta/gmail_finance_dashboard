
# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
import csv 
  
# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

if os.path.exists('token.pickle'):
  
        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

service = build('gmail', 'v1', credentials=creds)

def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    try:
        for msg in messages[:1]:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            # print(payload.keys())
            # use this for from emails
            # print(payload['parts'][0]['body']['data'])
            # use this for label>>
            # data= payload['body']['data']
            
            # data = data.replace("-","+").replace("_","/")
            # decoded_data = base64.b64decode(data)
            # soup = BeautifulSoup(decoded_data , "lxml")
            # body = soup.body()
            # print(body)

    except:
        pass         
search_messages(service=service,query='from:write2rukesh@gmail.com')
