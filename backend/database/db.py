import os
import tempfile
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():

    ca_cert = os.getenv("DB_SSL_CA")

    ssl_ca_path = None

    if ca_cert:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".pem",
            delete=False
        ) as f:
            f.write(ca_cert)
            ssl_ca_path = f.name

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca=ssl_ca_path,
        ssl_verify_cert=True
    )

    return connection