
# import the required libraries
from email import message
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
            print(messages[0])
    try:
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            if 'parts' in payload.keys():
                parts = payload.get('parts')[1]
                data = parts['body']['data']
                data = data.replace("-","+").replace("_","/")
                decoded_data = base64.b64decode(data)
                soup = BeautifulSoup(decoded_data , "html.parser")
                body = soup.body()
                print(body)
                print('\n')
                print('\n End of message')
            else:
                pass     

            
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
search_messages(service=service,query='label:city "transaction alert"')
