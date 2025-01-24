import pandas as pd
import json
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score
import time

# Lista de stop words para português
stop_words_pt = [
    'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 
    'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando', 
    'muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'era', 
    'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'estão', 'você', 'tinha', 
    'foram', 'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'têm', 'numa', 'pelos', 'elas', 'havia', 'seja', 'qual', 
    'será', 'nós', 'tenho', 'lhe', 'deles', 'essas', 'esses', 'pelas', 'este', 'fosse', 'dele', 'tu', 'te', 'vocês', 
    'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas', 'dela', 'delas', 
    'esta', 'estes', 'estas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'aquilo', 'estou', 'está', 'estamos', 
    'estão', 'estive', 'esteve', 'estivemos', 'estiveram', 'estava', 'estávamos', 'estavam', 'estivera', 'estivéramos', 
    'esteja', 'estejamos', 'estejam', 'estivesse', 'estivéssemos', 'estivessem', 'estiver', 'estivermos', 'estiverem', 
    'hei', 'há', 'havemos', 'hão', 'houve', 'houvemos', 'houveram', 'houvera', 'houvéramos', 'haja', 'hajamos', 'hajam', 
    'houvesse', 'houvéssemos', 'houvessem', 'houver', 'houvermos', 'houverem', 'houverei', 'houverá', 'houveremos', 
    'houverão', 'houveria', 'houveríamos', 'houveriam', 'sou', 'somos', 'são', 'era', 'éramos', 'eram', 'fui', 'foi', 
    'fomos', 'foram', 'fora', 'fôramos', 'seja', 'sejamos', 'sejam', 'fosse', 'fôssemos', 'fossem', 'for', 'formos', 
    'forem', 'serei', 'será', 'seremos', 'serão', 'seria', 'seríamos', 'seriam', 'tenho', 'tem', 'temos', 'tém', 'tinha', 
    'tínhamos', 'tinham', 'tive', 'teve', 'tivemos', 'tiveram', 'tivera', 'tivéramos', 'tenha', 'tenhamos', 'tenham', 
    'tivesse', 'tivéssemos', 'tivessem', 'tiver', 'tivermos', 'tiverem', 'terei', 'terá', 'teremos', 'terão', 'teria', 
    'teríamos', 'teriam', '<não há comentários do consumidor>', 'consumidor', 'comentários'
]

# Carrega e converte os dados do arquivo JSON para um DataFrame
with open('dados2025.json', 'r') as f:
    data = json.load(f)
df = pd.json_normalize(data)

print("Dados carregados com sucesso!")

# Conta as ocorrências de "<não há comentários do consumidor>"
num_nao_comentarios = df['comentario'].str.count('<não há comentários do consumidor>').sum()
print(f"Número de ocorrências de '<não há comentários do consumidor>': {num_nao_comentarios}")

# Filtra apenas comentários válidos e converte 'nota' para inteiro
df = df[(df['comentario'] != '<não há comentários do consumidor>') & (df['nota'].isin(['1', '2', '3', '4', '5']))]
df['nota'] = df['nota'].astype(int)
df['status'] = df['status'].map({'Resolvido': 1, 'Não Resolvido': 0})

# Limita o número de features para reduzir recursos
vectorizer = TfidfVectorizer(stop_words=stop_words_pt, max_features=500)
X_text = vectorizer.fit_transform(df['comentario'])

# Obtém os nomes das palavras associadas a cada índice no vetor TF-IDF
palavras = vectorizer.get_feature_names_out()

# Exibe as palavras associadas aos índices das colunas 295, 25 e 60
print("Palavra na coluna 295:", palavras[295])
print("Palavra na coluna 25:", palavras[25])
print("Palavra na coluna 60:", palavras[60])

# Converte a matriz para DataFrame e garante que todos os nomes de colunas são strings
X_text_df = pd.DataFrame(X_text.toarray())
X_text_df.columns = X_text_df.columns.astype(str)  # Convertendo para string para evitar problemas

# Concatena o vetor TF-IDF e a coluna status
X = pd.concat([X_text_df, df['status'].reset_index(drop=True)], axis=1)
y = df['nota']

# Calcula e exibe a proporção de classes
class_proportions = y.value_counts(normalize=True)
print("Proporção de classes:")
print(class_proportions)

# Divide os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Dimensoes dos dados de treino e teste:")
print(X_train.shape, X_test.shape)

print("Numero de classes:")
print(y_train.nunique())

# Configura a busca de hiperparâmetros simplificada
param_grid = {
    'n_estimators': [25, 50, 100, 200],
    'max_depth': [5, 10, 20, 40, None]
}
model = RandomForestClassifier(random_state=42, n_jobs=-1) #n_jobs=-1 significa que todos os processadores serão usados
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')

# Comeca a cronometrar o tempo decorrido
start = time.time()
print("Iniciando busca de hiperparâmetros...")
grid_search.fit(X_train, y_train)

# Faz previsões e avalia a acurácia
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
balanced_accuracy = balanced_accuracy_score(y_test, y_pred)

print(f'Acurácia do melhor modelo: {accuracy * 100:.2f}%')
print(f'Acurácia balanceada do melhor modelo: {balanced_accuracy * 100:.2f}%')
print("Melhores parâmetros:", grid_search.best_params_)

# Impressao das features mais importantes
importances = best_model.feature_importances_
indices = importances.argsort()[::-1]
print("Features mais importantes:")
for i in range(10):
    print(f'{X.columns[indices[i]]}: {importances[indices[i]]}')

# Encerra a cronometragem e exibe o tempo decorrido
end = time.time()
print(f"Tempo decorrido: {(end - start)/60:.2f} minutos")
