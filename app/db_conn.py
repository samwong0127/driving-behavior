import mysql.connector

def db_connection():
    mydb = mysql.connector.connect( host = 'database-1.cjoxdq5rc2hq.us-east-1.rds.amazonaws.com',
    user = 'admin',
    port = '3306',
    database = 'comp4442_project',
    passwd = '12345678',
    autocommit = True)
    return mydb

if __name__ == '__main__':
    db_connection()