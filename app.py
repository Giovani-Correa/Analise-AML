import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
import numpy as np

df_maio = pd.read_csv('data/data_limpos/transacoes_maio_2025_limpo.csv')
df_abril = pd.read_csv('data/data_limpos/transacoes_abril_limpo.csv')
df_junho = pd.read_csv('data/data_limpos/transacoes_junho_2025_limpo.csv')

df = pd.concat([df_abril, df_maio, df_junho], ignore_index=True)
#print(df)

df = pd.get_dummies(df, columns=['canal', 'cidade_transacao', 'cidade_origem'])
df['data_transacao'] = pd.to_datetime(df['data_transacao'], errors='coerce')
df['dia'] = df['data_transacao'].dt.day
df['mes'] = df['data_transacao'].dt.month
df['dia_semana'] = df['data_transacao'].dt.weekday
df['hora'] = df['data_transacao'].dt.hour

df.drop(columns=['id_transacao','id_cliente_origem','id_cliente_destino','data_transacao'], inplace=True)
#print(df)

X = df.drop(columns=['flag_suspeita']) 
y = df['flag_suspeita']

print(y.value_counts())

# Separar treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Treinar o modelo com RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
clf.fit(X_train, y_train)

# Treinar o modelo com LogisticRegression, por enquanto é o melhor
# clf = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
# clf.fit(X_train, y_train)



# Avaliar o modelo
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_true, y_prob))
print("PR AUC:", average_precision_score(y_true, y_prob))
print(confusion_matrix(y_test, y_pred))

# # 2. Filtrar apenas as linhas suspeitas
# df_suspeitas = df[df['flag_suspeita'] == 1].copy()

# # 3. Separar features e alvo para fraude confirmada
# X_fraude = df_suspeitas.drop(columns=['flag_fraude_confirmada'])
# y_fraude = df_suspeitas['flag_fraude_confirmada']

# # 4. Separar treino e teste
# Xf_train, Xf_test, yf_train, yf_test = train_test_split(X_fraude, y_fraude, test_size=0.2, random_state=42, stratify=y_fraude)

# # 5. Treinar modelo (pode usar RandomForest, LogisticRegression, etc)
# clf_fraude = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
# clf_fraude.fit(Xf_train, yf_train)

# # 6. Avaliar
# yf_pred = clf_fraude.predict(Xf_test)
# print(classification_report(yf_test, yf_pred))
# print(confusion_matrix(yf_test, yf_pred))
