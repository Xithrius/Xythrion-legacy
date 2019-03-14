#-----------------------------------------------------------------------------#
# Libraries
#-----------------------------------------------------------------------------
from direction import pathing
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
#/////////////////////////////////////////////////////////////////////////////#

#-----------------------------------------------------------------------------#
# Setting up environment.
#########################
# json, os
#-----------------------------------------------------------------------------
with open(pathing("credentials.json"), "r") as f:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json.load(f)
#/////////////////////////////////////////////////////////////////////////////#

#-----------------------------------------------------------------------------#
# Testing input and output google sheets
#########################
# oauth2client.service_account.ServiceAccountCredentials
#-----------------------------------------------------------------------------
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(pathing('credentials.json'), scope)
client = gspread.authorize(creds)

sheet = client.open('Connections').whatDo
information = sheet.get_all_records()
print(information)
#/////////////////////////////////////////////////////////////////////////////#
