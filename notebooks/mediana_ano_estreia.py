import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PIL._imaging import display

from main import conn


'''Qual a Mediana de Avaliação dos Filmes Em Relação ao Ano de Estréia?'''

# Consulta SQL
consulta4 = '''
            SELECT rating AS Rating, premiered FROM 
            ratings JOIN titles ON ratings.title_id = titles.title_id 
            WHERE premiered <= 2022 AND type = 'movie'
            ORDER BY premiered
            '''

# Resultado
resultado4 = pd.read_sql_query(consulta4, conn)


display(resultado4)

# Calculamos a mediana ao longo do tempo (anos)
ratings = []
for year in set(resultado4['premiered']):
    ratings.append(np.median(resultado4[resultado4['premiered'] == year]['Rating']))

    type(ratings)

    print(ratings[1:10])

    # Lista de anos
    anos = list(set(resultado4['premiered']))

    print(anos[1:10])

    # Plot
    plt.figure(figsize=(16, 8))
    plt.plot(anos, ratings)
    plt.xlabel('\nAno')
    plt.ylabel('Mediana de Avaliação')
    plt.title('\nMediana de Avaliação dos Filmes Em Relação ao Ano de Estréia\n')
    plt.show()

