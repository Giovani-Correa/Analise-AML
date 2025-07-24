import pandas as pd
import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os
from time import time
import traceback

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Parâmetros de conexão
host = os.getenv("MYSQL_HOST")
port = int(os.getenv("MYSQL_PORT"))  
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

def enviar_dados(dataframe, tabela):
    try:
        if dataframe.empty:
            st.warning(f"O DataFrame está vazio. Nada será enviado para a tabela '{tabela}'.")
            return

        # Garante que a coluna 'dado' existe com valor padrão False
        if "dado" not in dataframe.columns:
            dataframe["dado"] = 'FALSO'
        else:
            nulls = dataframe["dado"].isnull().sum()
            if nulls > 0:
                st.info(f"{nulls} valores nulos encontrados na coluna 'dado'. Preenchendo com 'FALSO'.")
            dataframe["dado"] = dataframe["dado"].fillna(False)

        # Conecta ao banco
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        # Converter colunas datetime para string
        datetime_cols = dataframe.select_dtypes(include=['datetime64[ns]', 'datetime64', 'timedelta64']).columns
        for col in datetime_cols:
            dataframe[col] = dataframe[col].astype(str)

        # Converter para lista de tuplas
        dados = [tuple(x) for x in dataframe.to_numpy()]
        colunas = ", ".join(dataframe.columns)
        valores = ", ".join(["%s"] * len(dataframe.columns))
        sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})"

        # Inserir dados no stage
        st.info(f"Iniciando inserção de {len(dados)} registros na tabela '{tabela}'...")
        start_time = time()
        cursor.executemany(sql, dados)
        conn.commit()
        st.success(f"Inserção concluída: {len(dados)} registros na tabela '{tabela}' em {time()-start_time:.2f}s")

        # Se for para o stage, replica para o core
        if tabela == "dw_stage.transacao":
            try:
                cursor.execute("USE dw_core;")
                st.info("Enviando dados para 'dw_core.transacao' sem duplicar registros...")

                # Inserção ignorando duplicados (com base em UNIQUE/PK no banco)
                cursor.execute("INSERT IGNORE INTO dw_core.transacao SELECT * FROM dw_stage.transacao;")


                conn.commit()

                st.success("Dados enviados para 'dw_core.transacao' com sucesso (sem duplicados).")

            except Exception as e:
                st.error("Erro ao enviar dados para o core.")
                st.exception(e)


    except Exception as e:
        st.error("Erro ao enviar dados.")
        print(f"Erro ao enviar dados: {e}")
        traceback.print_exc()

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

