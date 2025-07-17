import pandas as pd
import os

# Função para tratar os dados do csv recebido no import
def tratamento_geral(df: pd.DataFrame) -> pd.DataFrame:

    # Caminho absoluto baseado na localização deste arquivo
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_clientes = os.path.join(base_dir, '..', 'data', 'data_limpos', 'clientes_agencia_londrina_limpo.csv')
    caminho_clientes = os.path.normpath(caminho_clientes)

    df_clientes = pd.read_csv(caminho_clientes)


    #Verificar se há dados nulos
    print(df.isna().sum())

    #Verificar se há duplicatas
    duplicatas = df['id_transacao'].duplicated().any()
    print(f"Duplicatas: {duplicatas}")

    # Verificar nomes inconsistentes nas colunas 'cidade_transacao', 'canal' e 'cidade_origem'
    print(df['cidade_transacao'].unique())

    print(df['canal'].unique())

    print(df['cidade_origem'].unique())

    # Tratar se há valores de transação negativos ou 0
    df = df[df['valor'] > 0]

    # Converter coluna de data para datetime
    df['data_transacao'] = pd.to_datetime(df['data_transacao'])



    # Pegue os IDs válidos
    ids_validos = set(df_clientes['id_cliente'])

    # Filtre as transações onde ambos os clientes existem
    df = df[
        df['id_cliente_origem'].isin(ids_validos)
    ]

    # Adicionar coluna com o número do mês
    meses_unicos = df['data_transacao'].dt.month.unique()
    anos_unicos = df['data_transacao'].dt.year.unique()

    print("Meses encontrados:", meses_unicos)
    print("Anos encontrados:", anos_unicos)


    # Verificação se a coluna 'cidade origem' é mesmo redundante
    df_join = df.merge(
        df_clientes,
        left_on='id_cliente_origem',
        right_on='id_cliente' 
    )

    df_test = df_join['cidade_origem'] == df_join['cidade_residencia']
    print('Soma')
    print(df_test.sum())  # Quantas batem


    # drop na coluna 'cidade_origem'
    df.drop(columns=['cidade_origem'], inplace=True)
    print(df.columns)

    meses_predominantes = df['data_transacao'].dt.month.mode()
    mes_predominante = meses_predominantes[0] if not meses_predominantes.empty else 'desconhecido'
    anos_predominantes = df['data_transacao'].dt.year.mode()
    ano_predominante = anos_predominantes[0] if not anos_predominantes.empty else 'desconhecido'

    # # Caminho absoluto para salvar o arquivo
    # caminho_saida = os.path.join(base_dir, '..', 'data', 'data_limpos', f'transacoes_{mes_predominante}_{ano_predominante}_limpo2.csv')
    # caminho_saida = os.path.normpath(caminho_saida)

    # # Garante que a pasta existe
    # os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    # # Salvar o DataFrame limpo em um novo arquivo CSV
    # df.to_csv(caminho_saida, index=False)

    return df