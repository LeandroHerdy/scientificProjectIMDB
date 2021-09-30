import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from main import conn
from mediana import retorna_generos


'''Qual a Relação Entre Duração e Gênero?'''

# Consulta SQL
consulta7 = '''
            SELECT AVG(runtime_minutes) Runtime, genres 
            FROM titles 
            WHERE type = 'movie'
            AND runtime_minutes != 'NaN'
            GROUP BY genres
            '''

# Resultado
resultado7 = pd.read_sql_query(consulta7, conn)

# Retorna gêneros únicos
generos_unicos = retorna_generos(resultado7)

# Visualiza
print(generos_unicos)

# Calcula duração por gênero
genero_runtime = []
for item in generos_unicos:
    consulta = 'SELECT runtime_minutes Runtime FROM  titles  WHERE genres LIKE '+ '\''+'%'+item+'%'+'\' AND type=\'movie\' AND Runtime!=\'NaN\''
    resultado = pd.read_sql_query(consulta, conn)
    genero_runtime.append(np.median(resultado['Runtime']))

# Prepara o dataframe
df_genero_runtime = pd.DataFrame()
df_genero_runtime['genre'] = generos_unicos
df_genero_runtime['runtime'] = genero_runtime

# Remove índice 18 (news)
df_genero_runtime = df_genero_runtime.drop(index=18)

# Ordena os dados
df_genero_runtime = df_genero_runtime.sort_values(by='runtime', ascending=False)


# Plot

# Tamanho da figura
plt.figure(figsize=(16, 8))

# Barplot
sns.barplot(y=df_genero_runtime.genre, x=df_genero_runtime.runtime, orient="h")

# Loop
for i in range(len(df_genero_runtime.index)):
    plt.text(df_genero_runtime.runtime[df_genero_runtime.index[i]],
             i + 0.25,
             round(df_genero_runtime["runtime"][df_genero_runtime.index[i]], 2))

plt.ylabel('Gênero')
plt.xlabel('\nMediana de Tempo de Duração (Minutos)')
plt.title('\nRelação Entre Duração e Gênero\n')
plt.show()
