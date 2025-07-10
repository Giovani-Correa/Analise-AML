import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
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

# # Criar banco BANKING
# try:
#     conn = psycopg2.connect(dbname=default_db, user=user, password=password, host=host, port=port)
#     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     cur = conn.cursor()
#     cur.execute(f'CREATE DATABASE "{db_name}"')
#     print(f" Banco '{db_name}' criado.")
#     cur.close()
#     conn.close()
# except Exception as e:
#     print(" Banco já existe ou erro:", e)

# Conectar ao banco BANKING
try:
    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
    print(f" Conectado ao banco '{db_name}'.")
    conn.close()
except Exception as e:
    print(" Erro ao conectar:", e)
