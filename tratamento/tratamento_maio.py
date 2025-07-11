import pandas as pd

# ler arquivo CSV do mês de maio
df_maio = pd.read_csv('../data/transacoes_maio_2025.csv')
df_clientes = pd.read_csv('../data/data_limpos/clientes_agencia_londrina_limpo.csv')
#Verificar se há dados nulos no mês de maio
print(df_maio.isna().sum())

# Verificar se há duplicatas nos clientes
existe_duplicatas = df_maio['id_transacao'].duplicated().any()
print(f"Duplicatas: {existe_duplicatas}")

# Adicionar coluna 'mes' com valor 'maio'
df_maio['mes'] = 'maio'
print(df_maio)

# Verificar nomes inconsistentes nas colunas 'cidade_transacao', 'canal' e 'cidade_origem'
print(df_maio['cidade_transacao'].unique())

print(df_maio['canal'].unique())

print(df_maio['cidade_origem'].unique())

# Tratar se há valores de transação negativos ou 0
df_maio = df_maio[df_maio['valor'] > 0]

# Converter coluna de data para datetime
df_maio['data_transacao'] = pd.to_datetime(df_maio['data_transacao'])

# Pegue os IDs válidos
ids_validos = set(df_clientes['id_cliente'])

# Filtre as transações onde ambos os clientes existem
df_maio = df_maio[
    df_maio['id_cliente_origem'].isin(ids_validos) 
]

# Salvar o DataFrame limpo em um novo arquivo CSV
df_maio.to_csv('../data/data_limpos/transacoes_maio_2025_limpo.csv', index=False)

