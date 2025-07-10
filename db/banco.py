import psycopg2
from dotenv import load_dotenv
import os

# Carregar .env do caminho correto
load_dotenv(dotenv_path="./db/.env")  

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
default_db = os.getenv("DB_DEFAULT")
db_name = os.getenv("DB_NAME")

# Conecta ao banco
try:
    conn = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print(f"✅ Conectado ao banco '{db_name}' no servidor {host}")
    conn.close()
except Exception as e:
    print("❌ Erro ao conectar:", e)