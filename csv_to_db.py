import pandas as pd
from sqlalchemy import create_engine
import urllib
import re
import pyodbc

# Load your scraped data
df = pd.read_csv("lowongan_remote.csv")

# Data Cleaning
def clean_salary(text, get_max=False):
    # Cari semua angka di dalam teks (misal: ['7000000', '8000000'])
    numbers = re.findall(r'\d+', text.replace('.', '').replace(',', ''))
    if len(numbers) >= 2:
        return numbers[1] if get_max else numbers[0]
    elif len(numbers) == 1:
        return numbers[0] if not get_max else None
    return None

df['Min_Salary'] = df['Salary'].apply(lambda x: clean_salary(str(x), False))
df['Max_Salary'] = df['Salary'].apply(lambda x: clean_salary(str(x), True))

# SQL Server Connection Setup
SERVER_NAME = 'xx.xx.2.23' # Bukan nama server sebenarnya (hanya sbg contoh) 
DATABASE_NAME = 'projects'
USERNAME = 'sa'
PASSWORD = 'Passwordcontoh123!' # Bukan password sebenarnya (hanya sbg contoh)
TABLE_NAME = 'remote_jobs'

# String connection for SQL Server Authentication
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};" # Ganti drivernya ke versi 17
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;" # Ini kunci untuk melewati SSL Error 18
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Load data to SQL
try:
    df.to_sql(TABLE_NAME, schema='dbo', con=engine, if_exists='replace', index=False)
    print(f"✅ Success! {len(df)} rows uploaded to table: {TABLE_NAME}")
except Exception as e:
    print(f"❌ Error: {e}")