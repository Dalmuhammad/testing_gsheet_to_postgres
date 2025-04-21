from sqlalchemy import text
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from datetime import datetime
from sqlalchemy import text
import gspread
import pandas as pd
import sqlalchemy
import numpy as np
import os
import urllib.parse as ur
import numpy as np
import re
import access as ac

# Google sheet connection
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]
script_directory = os.path.dirname(os.path.abspath(__file__))
cred_json = os.path.join(script_directory, 'credentials_serviceaccount.json')
credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_json,scopes=scope)
gc = gspread.authorize(credentials)


# Set up variable
xlsx_file_id = ac.testing_gsheet_1  	        # ID file .xlsx on Google Drive
worksheet_name = 'Sales Dataset'                # Worsheet name on Google Sheets
schema_name = 'gsheet'                          # schema target
table_name = 'sheet1'                           # table target

'''
========================================================================
Ini kalau updload di google drive nya dalam bentuk xlxs.
========================================================================
'''
# # Create a Drive service
# drive_service = build('drive', 'v3', credentials=credentials)

# # Copy and convert the file to Google Sheets format
# copied_file = drive_service.files().copy(
#     fileId=xlsx_file_id,
#     body={"name": "Copy of Original", "mimeType": "application/vnd.google-apps.spreadsheet"}
# ).execute()

# # Get the new Google Sheets file's ID
# new_sheets_file_id = copied_file['id']

# # Use the new ID for reference if needed
# sheets_file_id = new_sheets_file_id

# # Access the new Google Sheets document
# spreadsheet = gc.open_by_key(sheets_file_id)

'''
========================================================================
'''

spreadsheet = gc.open('testing_gsheet_1')
worksheet = spreadsheet.worksheet(worksheet_name)
#values = worksheet.get_all_values()

#print columns
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:],columns=data[0],index=None)


'''
========================================================================
All usable functions store here
========================================================================
'''

#Clean header
def clean_header(df,chars,rep):
    for char in chars:
        df.columns=df.columns.str.replace(char,rep,regex=True)
    df.columns=[col.lower().strip() for col in df.columns]
    df.columns = df.columns.str.replace(r'_+', '_', regex=True)
    return df

# Convert new name for duplicated columns 
def change_duplicated_columns(df):
    cols = df.columns.tolist()
    dupes = {}
    for i, name in enumerate(cols):
        if name in dupes:
            dupes[name] += 1
            cols[i] = f"{name}_{dupes[name]}"
        else:
            dupes[name] = 0 
    df.columns = cols
    return df

# Function to convert variant date formats to yyyy-mm-dd
def date_conversion(date_string):
    if date_string is None or pd.isnull(date_string) or date_string == '':
        return None

    formats_to_try = ['%d-%b-%Y','%d/%m/%Y','%m/%d/%Y','%Y-%m-%d','%d %b %Y']  # Add more formats as needed

    months = {'Mei': 'May','Agu': 'Aug','Okt': 'Oct', 'Des': 'Dec'}

    for indo, eng in months.items():
        date_string = date_string.replace(indo, eng)

    for date_format in formats_to_try:
        try:
            date_obj = datetime.strptime(date_string, date_format)
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            pass

    # If no format matches, return None or handle the error as needed
    return None

def replace_data(schema,table):
    sqltruncate=f'truncate table {schema}.{table}'
    pg_conn.execute(text(sqltruncate))
    pg_conn.commit()

    df.to_sql(table,con=database_url,schema=schema_name,if_exists='append',index=False)

'''
========================================================================
'''

'''
==================================================
Define special columns
==================================================
'''
#pleace the column name with format test_nama_column
date_column=['order_date']

numeric_columns=['amount', 'profit', 'quantity']
'''
=======================================================
'''
#Bersihkan nama kolom
spec=[r'\n ','\t',' - ','-',r'\s+']
df = clean_header(df,spec, rep= '_')
df = change_duplicated_columns(df)

# Konversi kolom tanggal dengan proper format
for col in date_column:
    df[col]=df[col].apply(date_conversion)

# Konversi kolom ke numeric, untuk data yang tidak proper auto-null
for col in numeric_columns:
    df[col]=df[col].apply(pd.to_numeric,errors='coerce')
    df[col]=df[col].fillna(0)

#Drop null column
df.dropna(how='all', axis=0, subset=df.columns[(df.isin(['', ' ']) | df.isna()).any(axis=0)])

# print(df.dtypes)
# print(df)

# Construct connection to postgres
database_url = sqlalchemy.create_engine(
    f'postgresql://{ac.user}:{ur.quote(ac.pwd)}@{ac.host}:{ac.port}/{ac.database}'
)
pg_conn = database_url.connect()

print("Connected to PostgreSQL database.")


try:
    df.to_sql(name=table_name, con=database_url, schema=schema_name, if_exists='append', index=False)
except Exception as e:
    pg_conn.rollback()
    print(f'There is an error of {table_name} data processing: {e}')
    raise
else:
    replace_data(schema=schema_name,table=table_name)
pg_conn.close()
database_url.dispose()

print("success")