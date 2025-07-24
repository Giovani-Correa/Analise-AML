import streamlit as st
import pandas as pd
from db.salva_banco import enviar_dados

from tratamento.tratamento_geral import tratamento_geral
from script.machine import categorizar_csv, predicao

st.set_page_config(page_title="LondriBank - Análise de Fraudes", page_icon="./img/icon.png", layout="wide")

col1_logo, col2_logo, col3_logo = st.columns([4, 2, 4])
with col2_logo:
    st.image('./img/LondriBank.png', width=300)

def divider(cor="#000000", altura="2px", largura="100%"):
    st.markdown(
        f'<hr style="border: none; height: {altura}; background-color: {cor}; width: {largura}; margin: 20px 0;">',
        unsafe_allow_html=True
    )
divider(cor="#EC8A14", altura="3px", largura="100%")

def load_css():
    try:
        with open("styles/custom.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Arquivo 'styles/custom.css' não encontrado. O estilo padrão do Streamlit será usado.")

load_css()

st.title("CSV File Importer")
st.markdown("Envie o CSV para análise de dados e visualização.")

uploaded_file = st.file_uploader("Envie o Arquivo CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    try:
        df_tratado = tratamento_geral(df.copy())
        df_class = categorizar_csv(df_tratado.copy())
        df_previsto = predicao(df_class.copy(), df_tratado.copy())
    except Exception as e:
        st.error(f"Ocorreu um erro durante o processamento dos dados: {e}")
        st.info("Por favor, verifique se as funções 'tratamento_geral', 'categorizar_csv' e 'predicao' em seus respectivos arquivos estão retornando um DataFrame.")
        st.stop()

    if 'flag_suspeita' not in df_previsto.columns:
        st.error("A coluna 'flag_suspeita' não foi encontrada no DataFrame após o processamento. Verifique sua função 'tratamento_geral'.")
    else:
        df_suspeitas = df_previsto[df_previsto['flag_suspeita'] == 1].copy()

        if 'flag_fraude_confirmada' not in df_suspeitas.columns:
            df_suspeitas['flag_fraude_confirmada'] = False
        st.write("### Transações Suspeitas para Confirmação:")

        if not df_suspeitas.empty:

            column_configurations = {col: st.column_config.Column(disabled=True) for col in df_suspeitas.columns}

            column_configurations["flag_fraude_confirmada"] = st.column_config.CheckboxColumn(
                "Confirmar Suspeita",
                help="Marque para confirmar se a transação é realmente suspeita.",
                default=False,
                required=True,
                disabled=False 
            )

            edited_df = st.data_editor(
                df_suspeitas,
                column_config=column_configurations,
                hide_index=True,
                use_container_width=True
            )

            df_previsto = df_previsto[df_previsto['flag_suspeita'] != 1]
            df_previsto['flag_fraude_confirmada'] = 0
            df_completo = pd.concat([df_previsto,edited_df], ignore_index=True)
            
            csv_data = df_completo.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="transacoes_confirmadas.csv",
                mime="text/csv",
                help="Clique para baixar o CSV com as confirmações de suspeita."
            )

            botao_banco = st.button('Enviar para o Banco')

            if botao_banco:
                enviar_dados(df_completo,'dw_stage.transacao')



        else:
            st.info("Nenhuma transação suspeita encontrada para confirmação.")