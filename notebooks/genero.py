import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL._imaging import display

from sklearn.feature_extraction.text import CountVectorizer


from main import conn


'''Qual o Número de Títulos Por Gênero?'''

# Cria a consulta SQL
consulta2 = '''SELECT genres, COUNT(*) FROM titles WHERE type = 'movie' GROUP BY genres'''

# Resultado
resultado2 = pd.read_sql_query(consulta2, conn)

# Visualiza o resultado
print(display(resultado2))

# Converte as strings para minúsculo
resultado2['genres'] = resultado2['genres'].str.lower().values

# Remove valores NA (ausentes)
temp = resultado2['genres'].dropna()

# Criar um vetor usando expressão regular para filtrar as strings

# https://docs.python.org/3.8/library/re.html
padrao = '(?u)\\b[\\w-]+\\b'

# https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
vetor = CountVectorizer(token_pattern=padrao, analyzer='word').fit(temp)

type(vetor)

# Aplica a vetorização ao dataset sem valores NA
bag_generos = vetor.transform(temp)

type(bag_generos)

# Retorna gêneros únicos
generos_unicos = vetor.get_feature_names()

# Cria o dataframe de gêneros
generos = pd.DataFrame(bag_generos.todense(), columns=generos_unicos, index=temp.index)

# Visualiza
generos.info()

# Drop da coluna n
generos = generos.drop(columns='n', axis=0)

# Calcula o percentual
generos_percentual = 100 * pd.Series(generos.sum()).sort_values(ascending=False) / generos.shape[0]

# Visualiza
generos_percentual.head(10)

# Plot
plt.figure(figsize=(16, 8))
sns.barplot(x=generos_percentual.values, y=generos_percentual.index, orient="h", palette="terrain")
plt.ylabel('Gênero')
plt.xlabel("\nPercentual de Filmes (%)")
plt.title('\nNúmero (Percentual) de Títulos Por Gênero\n')
plt.show()
