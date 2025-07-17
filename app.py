import streamlit as st
import pandas as pd
from tratamento.tratamento_geral import tratamento_geral
from script.machine import categorizar_csv, predicao

# Config da Página
st.set_page_config(page_title="CSV Importer", page_icon="📊", layout="wide")

# Carregar css
def load_css():
    with open("styles/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Titulo da aplicação
st.title("CSV File Importer")
st.markdown("Envie o CSV para análise de dados e visualização.")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Envie o Arquivo CSV", type="csv")

if uploaded_file is not None:
    # Ler o arquivo CSV
    df = pd.read_csv(uploaded_file)

    df_tratado = tratamento_geral(df)

    df_class = categorizar_csv(df_tratado)

    df_previsto = predicao(df_class, df_tratado)
    
    # Mostrar o DataFrame tratado
    st.write("### Data Preview:")
    st.dataframe(df_previsto)

    # Mostrar estatísticas básicas
    st.write("### Basic Statistics:")
    st.write(df_previsto.describe())

    # Shape do dataframe
    st.write("### Data Shape:")
    st.write(df_previsto.shape)