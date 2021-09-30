import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL._imaging import display

from sklearn.feature_extraction.text import CountVectorizer


from main import conn


'''Qual a Mediana de Avaliação dos Filmes Por Gênero?'''

# Consulta SQL
consulta3 = '''
            SELECT rating, genres FROM 
            ratings JOIN titles ON ratings.title_id = titles.title_id 
            WHERE premiered <= 2022 AND type = 'movie'
            '''

# Resultado
resultado3 = pd.read_sql_query(consulta3, conn)

# Visualiza
display(resultado3)


# Função para retornar os genêros
def retorna_generos(df):
    df['genres'] = df['genres'].str.lower().values
    temp = df['genres'].dropna()
    vetor = CountVectorizer(token_pattern='(?u)\\b[\\w-]+\\b', analyzer='word').fit(temp)
    generos_unicos = vetor.get_feature_names()
    generos_unicos = [genre for genre in generos_unicos if len(genre) > 1]
    return generos_unicos


# Aplica a função
generos_unicos = retorna_generos(resultado3)

# Visualiza
generos_unicos

# Cria listas vazias
genero_counts = []
genero_ratings = []

# Loop
for item in generos_unicos:
    # Retorna a contagem de filmes por gênero
    consulta = 'SELECT COUNT(rating) FROM ratings JOIN titles ON ratings.title_id=titles.title_id WHERE genres LIKE ' + '\'' + '%' + item + '%' + '\' AND type=\'movie\''
    resultado = pd.read_sql_query(consulta, conn)
    genero_counts.append(resultado.values[0][0])

    # Retorna a avaliação de filmes por gênero
    consulta = 'SELECT rating FROM ratings JOIN titles ON ratings.title_id=titles.title_id WHERE genres LIKE ' + '\'' + '%' + item + '%' + '\' AND type=\'movie\''
    resultado = pd.read_sql_query(consulta, conn)
    genero_ratings.append(np.median(resultado['rating']))

# Prepara o dataframe final
df_genero_ratings = pd.DataFrame()
df_genero_ratings['genres'] = generos_unicos
df_genero_ratings['count'] = genero_counts
df_genero_ratings['rating'] = genero_ratings

# Visualiza
df_genero_ratings.head(20)

# Drop do índice 18 (news)
# Não queremos essa informação como gênero
df_genero_ratings = df_genero_ratings.drop(index=18)

# Ordena o resultado
df_genero_ratings = df_genero_ratings.sort_values(by='rating', ascending=False)

# Plot

# Figura
plt.figure(figsize=(16, 10))

# Barplot
sns.barplot(y=df_genero_ratings.genres, x=df_genero_ratings.rating, orient="h")

# Textos do gráfico
for i in range(len(df_genero_ratings.index)):
    plt.text(4.0,
             i + 0.25,
             str(df_genero_ratings['count'][df_genero_ratings.index[i]]) + " filmes")

    plt.text(df_genero_ratings.rating[df_genero_ratings.index[i]],
             i + 0.25,
             round(df_genero_ratings["rating"][df_genero_ratings.index[i]], 2))

plt.ylabel('Gênero')
plt.xlabel('Mediana da Avaliação')
plt.title('\nMediana de Avaliação Por Gênero\n')
plt.show()
