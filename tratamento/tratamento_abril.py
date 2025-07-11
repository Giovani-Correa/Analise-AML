import pandas as pd

# ler arquivo CSV mês de abril
df_abril=pd.read_csv('../data/transacoes_abril_2025.csv')
# ler arquivo CSV do CLiente
df_clientes = pd.read_csv('../data/data_limpos/clientes_agencia_londrina_limpo.csv')

#Verificar se há dados nulos no mês de maio
print(df_abril.isna().sum())

#Verificar se há duplicatas no mês de abril
duplicatas_abril = df_abril['id_transacao'].duplicated().any()
print(f"Duplicatas: {duplicatas_abril}")

# Adicionar coluna 'mes' com valor 'abril'
df_abril['mes'] = 'abril'
print(df_abril)

# Verificar nomes inconsistentes nas colunas 'cidade_transacao', 'canal' e 'cidade_origem'
print(df_abril['cidade_transacao'].unique())

print(df_abril['canal'].unique())

print(df_abril['cidade_origem'].unique())

# Tratar se há valores de transação negativos ou 0
df_abril = df_abril[df_abril['valor'] > 0]

# Converter coluna de data para datetime
df_abril['data_transacao'] = pd.to_datetime(df_abril['data_transacao'])


# Pegue os IDs válidos
ids_validos = set(df_clientes['id_cliente'])

# Filtre as transações onde ambos os clientes existem
df_abril = df_abril[
    df_abril['id_cliente_origem'].isin(ids_validos)
]


# Salvar o DataFrame limpo em um novo arquivo CSV
df_abril.to_csv('../data/data_limpos/transacoes_abril_limpo.csv', index=False)