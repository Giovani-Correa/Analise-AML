import mysql.connector
from dotenv import load_dotenv
import os

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
cursor.execute(""" 

    CREATE TABLE IF NOT EXISTS cliente (
        id_cliente VARCHAR(50) PRIMARY KEY NOT NULL,
        nome VARCHAR(50) NOT NULL,
        data_nascimento DATE NOT NULL,
        cidade_residencia VARCHAR(50) NOT NULL,
        tipo_conta ENUM('Corrente', 'Poupança', 'Empresarial') NOT NULL,
        pessoa_fisica ENUM('Sim', 'Não') NOT NULL,
        score_credito INT(3) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS transacao (
        id_transacao VARCHAR(50) PRIMARY KEY NOT NULL,
        id_cliente_origem VARCHAR(50) NOT NULL,
        id_cliente_destino VARCHAR(50) NOT NULL,
        data_transacao DATETIME NOT NULL,
        valor DECIMAL(10,2) NOT NULL,
        canal VARCHAR(50) NOT NULL,
        cidade_transacao VARCHAR(50) NOT NULL,
        flag_suspeita BOOLEAN NOT NULL,
        flag_fraude_confirmada BOOLEAN NOT NULL,
        dado ENUM("FALSO","REAL") NOT NULL,      
        FOREIGN KEY (id_cliente_origem) REFERENCES cliente(id_cliente)
        
    );
""")

