import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

df_cliente = pd.read_csv(r"C:\Users\André Ciccozzi\OneDrive\Documentos\Banking\Analise-AML\data\data_limpos\clientes_agencia_londrina_limpo.csv")

df_abril = pd.read_csv(r"C:\Users\André Ciccozzi\OneDrive\Documentos\Banking\Analise-AML\data\data_limpos\transacoes_abril_limpo.csv")

df_junho = pd.read_csv(r"C:\Users\André Ciccozzi\OneDrive\Documentos\Banking\Analise-AML\data\data_limpos\transacoes_junho_2025_limpo.csv")

df_maio = pd.read_csv(r"C:\Users\André Ciccozzi\OneDrive\Documentos\Banking\Analise-AML\data\data_limpos\transacoes_maio_2025_limpo.csv")

load_dotenv()  # carrega o .env da mesma pasta do script

host = os.getenv("MYSQL_HOST")
port = int(os.getenv("MYSQL_PORT"))  
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

conn = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

cursor = conn.cursor()

for _, row in df_cliente.iterrows():
    cursor.execute(
        "INSERT INTO cliente (id_cliente, nome, data_nascimento, cidade_residencia, tipo_conta, pessoa_fisica, score_credito) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (row['id_cliente'], row['nome'], row['data_nascimento'], row['cidade_residencia'], row['tipo_conta'], row['pessoa_fisica'], row['score_credito'])
    )


for df in [df_abril, df_maio, df_junho]:
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO transacao (id_transacao, id_cliente_origem, id_cliente_destino, data_transacao, valor, canal, cidade_transacao, cidade_origem, flag_suspeita, flag_fraude_confirmada, mes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (row['id_transacao'], row['id_cliente_origem'], row['id_cliente_destino'], row['data_transacao'], row['valor'], row['canal'], row['cidade_transacao'], row['cidade_origem'], row['flag_suspeita'], row['flag_fraude_confirmada'], row['mes'])
        )


conn.commit()
cursor.close()
conn.close()

