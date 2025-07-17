import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, average_precision_score
from imblearn.over_sampling import SMOTE
import joblib

# Função para prever dados novos
def predicao(df_machine, df_tratado):
    # Carregar modelo
    clf = joblib.load('script/modelo_randomforest.pkl')
    # Previsão
    df_tratado['flag_suspeita'] = clf.predict(df_machine)
    # Salvar com as previsões
    # df.to_csv("novo_arquivo_com_predicao.csv", index=False)
    return df_tratado

# Função para adequar o csv
def categorizar_csv(df):
    # Transformação de colunas categóricas em numéricas
    df = pd.get_dummies(df, columns=['canal', 'cidade_transacao'])

    # Separação do datetime em mes, dia, dia da semana e hora
    df['data_transacao'] = pd.to_datetime(df['data_transacao'], errors='coerce')
    df['dia'] = df['data_transacao'].dt.day
    df['mes'] = df['data_transacao'].dt.month
    df['dia_semana'] = df['data_transacao'].dt.weekday
    df['hora'] = df['data_transacao'].dt.hour

    # Remoção de colunas não usadas para o ML    
    cols_to_drop = ['id_transacao','id_cliente_origem','id_cliente_destino','data_transacao','flag_fraude_confirmada']
    df.drop(columns=[c for c in cols_to_drop if c in df.columns], inplace=True)

    return df  
    
# Leitura do csv
df_abril = pd.read_csv('data/data_limpos/transacoes_abril_2025_limpo.csv')
df_maio = pd.read_csv('data/data_limpos/transacoes_maio_2025_limpo.csv')
df_junho = pd.read_csv('data/data_limpos/transacoes_junho_2025_limpo.csv')

df = pd.concat([df_abril, df_maio, df_junho], ignore_index=True)

df = categorizar_csv(df)

# Separando a coluna flag_suspeita das outras
X = df.drop(columns=['flag_suspeita']) 
y = df['flag_suspeita']
# print(y.value_counts())

# Separar treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Balancear com SMOTE
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Treinar o modelo com RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
clf.fit(X_train_res, y_train_res)

# Avaliar o modelo
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_pred))
print("PR AUC:", average_precision_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

#Salvar modelo
joblib.dump(clf, 'script/modelo_randomforest.pkl')
print("\n✅ Modelo salvo!")