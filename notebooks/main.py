import sqlite3

import pandas as pd
import seaborn as sns
from PIL._imaging import display

import warnings

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")


# Conecta no banco de dados
conn = sqlite3.connect("imdb.db")

# Extrai a lista de tabelas
tabelas = pd.read_sql_query("SELECT NAME AS 'Table_Name' FROM sqlite_master WHERE type = 'table'", conn)

# Tipo do objeto
type(tabelas)

# Visualiza o resultado
tabelas.head()

# Vamos converter o dataframe em uma lista
tabelas = tabelas["Table_Name"].values.tolist()

# Percorrer a lista de tabelas no banco de dados e extrair o esquema de cada uma
for tabela in tabelas:
    consulta = "PRAGMA TABLE_INFO({})".format(tabela)
    resultado = pd.read_sql_query(consulta, conn)
    print("Esquema da tabela:", tabela)
    display(resultado)
    print("-" * 100)
    print("\n")
