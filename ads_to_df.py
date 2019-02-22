#script source: https://github.com/gsuitedevs/python-samples/blob/master/sheets/quickstart/quickstart.py
#modified by me

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

#Settings
SPREADSHEET_ID = '<<<<SPREADSHEET_ID_HERE>>>>>>>'
RANGE_NAME = 'Campaign!A1:E1000'
save_to = "<<<<<<<DIRECTORY>>>>>"

def ads_to_df():
    """Loads Data from a specified Google Spreadsheet (and saves it to a csv)
    """
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

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
	headers = values.pop(0)
    	df = pd.DataFrame(values, columns = headers)
	#df.to_csv(save_to + "ads_data.csv")
		
if __name__ == '__main__':
    ads_to_df()
