import mysql.connector
import os

def getConnection():
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ.get("database_password"),
    database="ecommerce_db"
    )
    return conn


