import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  # carrega o .env da mesma pasta do script

host = os.getenv("MYSQL_HOST")
port = int(os.getenv("MYSQL_PORT"))  # erro vinha daqui
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

try:
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    print(f"✅ Conectado ao banco '{database}' no servidor {host}:{port}")

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    for table in cursor.fetchall():
        print(f"- {table[0]}")

    cursor.close()
    conn.close()

except mysql.connector.Error as e:
    print("❌ Erro ao conectar:", e)
