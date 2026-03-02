import csv
from pathlib import Path
import sqlite3
import pandas as pd

caminho_arquivo = Path(__file__).parent / 'servidores_2026_03.csv'
caminho_db = Path(__file__).parent/ 'servidores_2026.db'
print(caminho_arquivo)

conn = sqlite3.connect(caminho_db)
cursor = conn.cursor()

cursor.execute('''
               create table if not exists
               servidores_2026(
                pkMatricula text primary key,
                nome text,
                cargo text,
                orgao text,
                salario text)
               ''')
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    leitor = csv.reader(arquivo, delimiter=";")
    cabecalho = leitor.__next__()
    print("Cabeçalho:", cabecalho)
    
    query_insert = '''
        INSERT INTO servidores_2026 (pkMatricula, nome, cargo, orgao, salario)
        VALUES (?, ?, ?, ?, ?)
        '''
    for linha in leitor:
        if len(linha) >= 5:
            valores_para_inserir = (linha[0], linha[1], linha[2], linha[3], linha[4])# Pega apenas as primeiras 5 colunas, para evitar qualquer problema com índices.
            cursor.execute(query_insert, valores_para_inserir)
conn.commit()

query_select = 'select * from servidores_2026'
df_servidores = pd.read_sql_query(query_select, conn)
print(df_servidores.head())

#--Início da limpeza dos dados--
df_servidores['salario'] = df_servidores['salario'].str.replace('R$', '').str.replace(',', '.').astype(float) #Remove o '$', por ser tratar de um caractere especial; troca a vírgula por ponto para converter para float e depois converte a coluna para tipo numérico.
df_servidores['nome'] = df_servidores['nome'].str.strip() # Limpa o espaço em branco no início e no final da string (nome do servidor).
df_servidores['cargo'] = df_servidores['cargo'].str.strip() # Limpa o espaço em branco no início e no final da string, assim como possíveis caracteres invisíveis (cargo do servidor).
df_servidores['orgao'] = df_servidores['orgao'].str.strip() #Assim como o campo 'cargo', faz a limpeza do campo 'orgao' para evitar problemas de análise futura.

print("Dados após a limpeza:")
print(df_servidores.info())

df_servidores.to_sql('servidores_2026', conn, if_exists='replace', index=False) # Sobrescreve a tabela no banco de dados com os dados já sanitizados.
print("Dados limpos e atualizados no banco de dados.") #Mensagem de confirmação de gravação dos dados sanitizados no banco de dados.

query_cleaned = 'select * from servidores_2026'
df_servidores_cleaned = pd.read_sql_query(query_cleaned, conn)

print(df_servidores_cleaned.head()) # Exibe as primeiras linhas do DataFrame para verificar a limpeza dos dados.

print("Tipagem dos dados após limpeza:")
print(df_servidores_cleaned.dtypes)