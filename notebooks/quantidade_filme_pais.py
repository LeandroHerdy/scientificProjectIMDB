import pycountry

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL._imaging import display

from main import conn


'''Qual o Número de Filmes Produzidos Por País?'''

# Consulta SQL
consulta8 = '''
            SELECT region, COUNT(*) Number_of_movies FROM 
            akas JOIN titles ON 
            akas.title_id = titles.title_id
            WHERE region != 'None'
            AND type = \'movie\'
            GROUP BY region
            '''

# Resultado
resultado8 = pd.read_sql_query(consulta8, conn)

print(display(resultado8))

# Shape
resultado8.shape

(232, 2)

# Número de linhas
resultado8.shape[0]

# Listas auxiliares
nomes_paises = []
contagem = []

# Loop para obter o país de acordo com a região
for i in range(resultado8.shape[0]):
    try:
        coun = resultado8['region'].values[i]
        nomes_paises.append(pycountry.countries.get(alpha_2 = coun).name)
        contagem.append(resultado8['Number_of_movies'].values[i])
    except:
        continue

# Prepara o dataframe
df_filmes_paises = pd.DataFrame()
df_filmes_paises['country'] = nomes_paises
df_filmes_paises['Movie_Count'] = contagem

# Ordena o resultado
df_filmes_paises = df_filmes_paises.sort_values(by = 'Movie_Count', ascending = False)

# Visualiza
df_filmes_paises.head(10)

# Plot

# Figura
plt.figure(figsize=(20, 8))

# Barplot
sns.barplot(y=df_filmes_paises[:20].country, x=df_filmes_paises[:20].Movie_Count, orient="h")

# Loop
for i in range(0, 20):
    plt.text(df_filmes_paises.Movie_Count[df_filmes_paises.index[i]]-1,
             i + 0.30,
             round(df_filmes_paises["Movie_Count"][df_filmes_paises.index[i]], 2))

plt.ylabel('País')
plt.xlabel('\nNúmero de Filmes')
plt.title('\nNúmero de Filmes Produzidos Por País\n')
plt.show()
