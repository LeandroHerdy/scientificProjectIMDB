import pandas as pd
import matplotlib.pyplot as plt

from PIL._imaging import display


from main import conn
from mediana import retorna_generos


'''Qual o Número de Filmes Avaliados Por Gênero Em Relação ao Ano de Estréia?'''

# Consulta SQL
consulta5 = '''SELECT genres FROM titles '''

# Resultado
resultado5 = pd.read_sql_query(consulta5, conn)

display(resultado5)

# Retorna gêneros únicos
generos_unicos = retorna_generos(resultado5)


# Visualiza o resultado
print(generos_unicos)

# Agora fazemos a contagem
genero_count = []
for item in generos_unicos:
    consulta = 'SELECT COUNT(*) COUNT FROM  titles  WHERE genres LIKE '+ '\''+'%'+item+'%'+'\' AND type=\'movie\' AND premiered <= 2022'
    resultado = pd.read_sql_query(consulta, conn)
    genero_count.append(resultado['COUNT'].values[0])

# Prepara o dataframe
df_genero_count = pd.DataFrame()
df_genero_count['genre'] = generos_unicos
df_genero_count['Count'] = genero_count

# Calcula os top 5
df_genero_count = df_genero_count[df_genero_count['genre'] != 'n']
df_genero_count = df_genero_count.sort_values(by='Count', ascending=False)
top_generos = df_genero_count.head()['genre'].values

# Plot

# Figura
plt.figure(figsize = (16,8))

# Loop e Plot
for item in top_generos:
    consulta = 'SELECT COUNT(*) Number_of_movies, premiered Year FROM  titles  WHERE genres LIKE '+ '\''+'%'+item+'%'+'\' AND type=\'movie\' AND Year <=2022 GROUP BY Year'
    resultado = pd.read_sql_query(consulta, conn)
    plt.plot(resultado['Year'], resultado['Number_of_movies'])

plt.xlabel('\nAno')
plt.ylabel('Número de Filmes Avaliados')
plt.title('\nNúmero de Filmes Avaliados Por Gênero Em Relação ao Ano de Estréia\n')
plt.legend(labels = top_generos)
plt.show()

