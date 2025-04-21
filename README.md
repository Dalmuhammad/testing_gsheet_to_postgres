# testing_gsheet_to_postgres

This project is used to connect to Google Sheets and interact with data, particularly with a PostgreSQL database.

## Folder Structure
testing_gsheet/  
├── pyscript/ # Python scripts for interacting with Google Sheets & database  
│   ├──access.py # Contains credentials and connection settings  
│   └──credentials_serviceaccount.json # Google Sheets API credentials  
│   └──sheet1.py # file for ETL process  
├── venv/ # Python virtual environment (should be ignored by git)  
├── requirements.txt # Python dependencies  
└── .gitignore # Git ignore file (ignores venv, access, credentials, etc.)


## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/testing_gsheet.git
   cd testing_gsheet

2. Set up a Python virtual environment:
   ```bash
   python -m venv venv

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Set up Google Sheets API credentials
   
5. Edit pyscript/access.py with your PostgreSQL database and Google Sheets configurations

## Configurations

In pyscript/access.py, you'll find the following configuration options for connecting to your PostgreSQL database and Google Sheets API:

PostgreSQL Database Configuration:
The variables in access.py should be populated with your PostgreSQL connection details:  
### Target Database - Postgres  
host = 'hostname'       # Replace with your database hostname (e.g., localhost)  
port = 5432             # PostgreSQL port (default: 5432)  
user = 'username'       # Database username  
pwd = 'connection_password'  # Database password  
database = 'db_name'    # Database name  
schema = 'schema_name'  # Schema name for the database

In access.py, you'll also set the Google Sheets document ID for the spreadsheet you want to access:  

testing_gsheet_1 = 'ID file'  # Replace with your Google Sheets file ID


To see the google sheet that i used, you can see in the following link:
https://docs.google.com/spreadsheets/d/1OlcEL18h9LpnuQ5Y3oUc2N_CsrqMxmTgd_MRR9RabNU/edit?usp=sharing
