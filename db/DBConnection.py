import mysql.connector


def getConnection():
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vardhan",
    database="ecommerce_db"
    )
    return conn


