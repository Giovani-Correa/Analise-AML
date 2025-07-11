import pandas as pd

# ler arquivo CSV do CLiente
df_clientes = pd.read_csv('../data/clientes_agencia_londrina.csv')

#Verificar se há nulos nos clientes
print(df_clientes.isna().sum())

# Remover linhas que tiverem incosistências 
df_cliente_clear = df_clientes[~df_clientes['data_nascimento'].str.startswith("EXT", na=False)]

#Verificar se há duplicatas nos clientes
existe_duplicatas = df_cliente_clear['id_cliente'].duplicated().any()
print(f"Duplicatas: {existe_duplicatas}")

# Exibir os tipos únicos de conta presentes no DataFrame limpo
print(df_cliente_clear['tipo_conta'].unique())
print(df_cliente_clear['pessoa_fisica'].unique())


# Remover espaços em branco das colunas 'tipo_conta' e 'pessoa_fisica'
for col in df_cliente_clear.select_dtypes(include=['object']):
    df_cliente_clear.loc[:, col] = df_cliente_clear[col].str.strip()

# Salvar o DataFrame limpo em um novo arquivo CSV
df_cliente_clear.to_csv('../data/data_limpos/clientes_agencia_londrina_limpo.csv', index=False)