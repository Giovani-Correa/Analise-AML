import pandas as pd

# ler arquivo CSV do mês de junho
df_junho = pd.read_csv('../data/transacoes_junho_2025.csv')

# ler arquivo CSV do CLiente
df_clientes = pd.read_csv('../data/data_limpos/clientes_agencia_londrina_limpo.csv')

#Verificar se há dados nulos no mês de junho
print(df_junho.isna().sum())

# Verificar se há duplicatas nos clientes
existe_duplicatas = df_junho['id_transacao'].duplicated().any()
print(f"Duplicatas: {existe_duplicatas}")



# Verificar nomes inconsistentes nas colunas 'cidade_transacao', 'canal' e 'cidade_origem'
print(df_junho['cidade_transacao'].unique())

print(df_junho['canal'].unique())

print(df_junho['cidade_origem'].unique())

# Tratar se há valores de transação negativos ou 0
df_junho = df_junho[df_junho['valor'] > 0]

# Converter coluna de data para datetime
df_junho['data_transacao'] = pd.to_datetime(df_junho['data_transacao'])

# Pegue os IDs válidos
ids_validos = set(df_clientes['id_cliente'])

# Filtre as transações onde ambos os clientes existem
df_junho = df_junho[
    df_junho['id_cliente_origem'].isin(ids_validos) 
]

meses_unicos = df_junho['data_transacao'].dt.month.unique()
anos_unicos = df_junho['data_transacao'].dt.year.unique()

print("Meses encontrados:", meses_unicos)
print("Anos encontrados:", anos_unicos)


# Salvar o DataFrame limpo em um novo arquivo CSV
df_junho.to_csv('../data/data_limpos/transacoes_junho_2025_limpo.csv', index=False)

