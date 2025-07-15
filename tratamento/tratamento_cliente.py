import pandas as pd

# ler arquivo CSV do Cliente
df_clientes = pd.read_csv('../data/clientes_agencia_londrina.csv')

print(df_clientes.shape[0])
print(' ')

# Verificar se há nulos nos clientes
print(df_clientes.isna().sum())
print(df_clientes.shape[0])

# Remover linhas com inconsistências (ex: data de nascimento começando com "EXT")
df_cliente_clear = df_clientes[~df_clientes['data_nascimento'].str.startswith("EXT", na=False)]
print(df_cliente_clear.shape[0])

# Verificar duplicatas
existe_duplicatas = df_cliente_clear['id_cliente'].duplicated().any()
print(f"Duplicatas: {existe_duplicatas}")

# Remover espaços em branco das colunas de texto
for col in df_cliente_clear.select_dtypes(include=['object']):
    df_cliente_clear.loc[:, col] = df_cliente_clear[col].str.strip()

# Remover títulos como Sr, Sra, Dr, Dra dos nomes
df_cliente_clear['nome'] = df_cliente_clear['nome'].str.replace(r'^(Sr|Sra|Dr|Dra|Srta)\.?\s+', '', regex=True)

# Mostrar tipos únicos após limpeza
print(df_cliente_clear['tipo_conta'].unique())
print(df_cliente_clear['pessoa_fisica'].unique())

# Salvar o DataFrame limpo
df_cliente_clear.to_csv('../data/data_limpos/clientes_agencia_londrina_limpo.csv', index=False)
print(df_cliente_clear.shape[0])
