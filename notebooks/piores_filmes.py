import pandas as pd

from PIL._imaging import display

from main import conn


'''Quais São os Top 10 Piores Filmes?'''

# Consulta SQL
consulta10 = '''
            SELECT primary_title AS Movie_Name, genres, rating
            FROM 
            titles JOIN ratings
            ON  titles.title_id = ratings.title_id
            WHERE titles.type = 'movie' AND ratings.votes >= 25000
            ORDER BY rating ASC
            LIMIT 10
            '''

# Resultado
top10_piores_filmes = pd.read_sql_query(consulta10, conn)

print(display(top10_piores_filmes))
