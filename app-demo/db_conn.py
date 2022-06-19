import mysql.connector
import os

from dotenv import load_dotenv
load_dotenv()

def db_connection():
    return mysql.connector.connect(host=os.getenv("DB_HOST"),
                                   user=os.getenv("DB_USER"),
                                   port=os.getenv("DB_PORT", 3306),
                                   database=os.getenv("DB_SCHEMA"),
                                   passwd=os.getenv("DB_PASS"),
                                   autocommit=True, pool_size=1, pool_name="mypool")
