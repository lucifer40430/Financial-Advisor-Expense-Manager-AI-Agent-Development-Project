import mysql.connector


def get_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kota@123",
        database="financial_advisor"
    )

    return connection