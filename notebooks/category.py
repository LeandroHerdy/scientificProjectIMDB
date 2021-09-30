import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PIL._imaging import display
from matplotlib import cm

from main import conn


"""Quais São as Categorias de Filmes Mais Comuns no IMDB?
Quais são os principais tipos(categorias) dos títulos(filmes)?"""

# Cria a consulta SQL
consulta1 = '''SELECT type, COUNT(*) AS COUNT FROM titles GROUP BY type'''

# Extrai o resultado
resultado1 = pd.read_sql_query(consulta1, conn)

# Visualiza o resultado
display(resultado1)

# Calcular o percentual para cada tipo
resultado1['percentual'] = (resultado1['COUNT'] / resultado1['COUNT'].sum()) * 100

# Visualiza o resultado
display(resultado1)

# Um gráfico com apenas 4 categorias:
# As 3 categorias com mais títulos e 1 categoria com todo o restante

# Cria um dicionário vazio
others = {}

# Filtra o percentual em 5% e soma o total
others['COUNT'] = resultado1[resultado1['percentual'] < 5]['COUNT'].sum()

# Grava o percentual
others['percentual'] = resultado1[resultado1['percentual'] < 5]['percentual'].sum()

# Ajusta o nome
others['type'] = 'others'

# Visualiza
print(others)

# Filtrar o dataframe de resultado
resultado1 = resultado1[resultado1['percentual'] > 5]

# Append com o dataframe de outras categorias
resultado1 = resultado1.append(others, ignore_index=True)

# Visualiza
plt.show.resultado1.head()

# Ajusta os labels
labels = [str(resultado1['type'][i])+' '+'['+str(round(resultado1['percentual'][i], 2)) +'%'+']' for i in resultado1.index]

# Plot

# Mapa de cores
# https://matplotlib.org/stable/tutorials/colors/colormaps.html
cs = cm.Set3(np.arange(100))

# Cria a figura
f = plt.figure()

# Pie Plot
plt.pie(resultado1['COUNT'], labeldistance=1, radius=3, colors=cs, wedgeprops=dict(width=0.8))
plt.legend(labels=labels, loc='center', prop={'size': 12})
plt.title("Distribuição de Títulos", loc='Center', fontdict={'fontsize': 20, 'fontweight': 20})
plt.show()
