import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # lê o arquivo .env e carrega as variáveis automaticamente


def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER", "avnadmin"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME", "defaultdb"),
        ssl_ca=os.environ.get("DB_SSL_CA", "ca.pem"),
    )
