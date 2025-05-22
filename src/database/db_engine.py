import mysql.connector as mysql
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_DATABASE"),
    port=os.getenv('DB_PORT')
)

cursor = conn.cursor()
