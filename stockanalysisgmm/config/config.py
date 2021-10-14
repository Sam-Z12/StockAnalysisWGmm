import json
from pathlib import Path

CONSUMER_KEY = ''
REDIRECT_URI = ''
ACCOUNT_NUMBER = ''
CURRENT_PATH = str(Path(__file__).absolute().parent)
CREDENTIALS_PATH = CURRENT_PATH + '/credPath.json'
#print(f"Credentials Path: {CREDENTIALS_PATH}")

ALPHA_VANTAGE_KEY = ''


#Used to create a new Credentials path json file
# json_obj = {}

# with open ('credPath.json', 'w') as jsonFile:
#     json.dump(json_obj, jsonFile)