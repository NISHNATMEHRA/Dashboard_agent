import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def connect_to_sheet(json_keyfile, spreadsheet_url, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    gc = gspread.authorize(credentials)

    spreadsheet = gc.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.worksheet(sheet_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)
