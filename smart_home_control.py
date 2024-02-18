import csv
from langchain.document_loaders.csv_loader import CSVLoader
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import GoogleCredentials

def search_for_api (action:str) -> str:
    result = ""
    # Read Device Control CSV File
    with open('/home/alan/python/sideproject/device_control_table.csv') as file:
        csv_reader = csv.DictReader(file)
        action_table = [row for row in csv_reader]
    # Seach for control actions
    for api in action_table:
        if (api['action'] == action):
            result = api['api']
            break
    return result

