import numpy as np
import pandas as pd

from PIL._imaging import display

from main import conn


'''Qual o Filme Com Maior Tempo de Duração? Calcule os Percentis.'''

# Consulta SQL
consulta6 = '''
            SELECT runtime_minutes Runtime 
            FROM titles 
            WHERE type = 'movie' AND Runtime != 'NaN'
            '''

# Resultado
resultado6 = pd.read_sql_query(consulta6, conn)

print(display(resultado6))

# Loop para cálculo dos percentis
for i in range(101):
    val = i
    perc = round(np.percentile(resultado6['Runtime'].values, val), 2)
    print('{} percentil da duração (runtime) é: {}'.format(val, perc))

# Refazendo a consulta e retornando o filme com maior duração
consulta6 = '''
            SELECT runtime_minutes Runtime, primary_title
            FROM titles 
            WHERE type = 'movie' AND Runtime != 'NaN'
            ORDER BY Runtime DESC
            LIMIT 1
            '''

resultado6 = pd.read_sql_query(consulta6, conn)

print(resultado6)

