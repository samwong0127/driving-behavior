import mysql.connector

def db_connection():
    mydb = mysql.connector.connect( host = 'your database endpoint',
    user = 'admin',
    port = 'your database port',
    database = 'database name',
    passwd = '12345678',
    autocommit = True)
    return mydb
