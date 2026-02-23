import csv
from pathlib import Path
import sqlite3
import pandas as pd

caminho_arquivo = Path(__file__).parent / 'ldo-2024.csv'
caminho_db = Path(__file__).parent / 'ldo_2024.db'
print(caminho_arquivo)

conexao = sqlite3.connect(caminho_db)
cursor = conexao.cursor()

cursor.execute('''
        create table if not exists ldo_2024(
               especificacao text,
               valor_corrente_2024 text,
               valor_constante_2024 text,
               perc_pib_2024 text)
''')

with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    leitor = csv.reader(arquivo, delimiter=";")
    cabecalho = next(leitor)
    print("Cabeçalho:", cabecalho)

    query_insert = '''
        INSERT INTO ldo_2024 (especificacao, valor_corrente_2024, valor_constante_2024, perc_pib_2024)
        VALUES (?, ?, ?, ?)
    '''
    for linha in leitor:
        # Pegamos apenas os 4 primeiros itens da lista para bater com nossa tabela
        # Se a linha tiver menos itens, isso evita erro de índice
        if len(linha) >= 4:
            valores_para_inserir = (linha[0], linha[1], linha[2], linha[3])
            cursor.execute(query_insert, valores_para_inserir)

# Efetiva as transações no banco de dados
conexao.commit()

query_select = 'select * from ldo_2024'
df_ldo = pd.read_sql_query(query_select, conexao)
print(df_ldo.head())

# --- ETAPA DE DATA QUALITY (LIMPEZA) ---

# 1. Limpando a coluna 'valor_corrente_2024'
df_ldo['valor_corrente_2024'] = (
    df_ldo['valor_corrente_2024']
    .str.replace('.', '', regex=False)  # Remove os pontos de milhar
    .str.replace('(', '-', regex=False) # Troca ( por sinal de menos
    .str.replace(')', '', regex=False)  # Remove o )
    .astype(float)
)

# 2. Limpando a coluna 'valor_constante_2024'
df_ldo['valor_constante_2024'] = (
    df_ldo['valor_constante_2024']
    .str.replace('.', '', regex=False)
    .str.replace('(', '-', regex=False)
    .str.replace(')', '', regex=False)
    .astype(float)
)

# 3. Limpando a coluna 'perc_pib_2024'
# Substituímos os hifens ('-') por '0', trocamos eventuais vírgulas por pontos (padrão americano para decimais no Python) e convertemos para float
df_ldo['perc_pib_2024'] = (
    df_ldo['perc_pib_2024']
    .str.replace('-', '0', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

# Imprime um resumo do DataFrame para confirmar os novos tipos de dados
print("\nTipos de dados após a limpeza:")
print(df_ldo.info())

df_ldo.to_sql('ldo_2024_limpo', conexao, if_exists='replace', index=False)
print("Tabela 'ldo_2024_limpo' criada com sucesso!")

# --- VALIDANDO O RESULTADO ---
print("\nLendo a tabela limpa direto do banco com Pandas:")
query_limpa = 'SELECT * FROM ldo_2024_limpo'
df_limpo_do_banco = pd.read_sql_query(query_limpa, conexao)

print(df_limpo_do_banco.head())

print("\nTipos de dados importados do banco (agora como números reais):")
print(df_limpo_do_banco.dtypes)

aminho_db = Path(__file__).parent / 'ldo_2024.db'


with sqlite3.connect(caminho_db) as conexao:
    query = "SELECT * FROM ldo_2024_limpo"
    df = pd.read_sql_query(query, conexao)

print("--- INÍCIO DA ANÁLISE COM PANDAS ---")

# 1. Informações gerais do DataFrame
print("\n1. Estrutura dos dados importados:")
print(f"Total de linhas: {df.shape[0]}")
print(f"Total de colunas: {df.shape[1]}")

# 2. Operações Matemáticas (Agregação)
total_corrente = df['valor_corrente_2024'].sum()
# Formatação profissional: separar milhares e definir duas casas decimais
print(f"\n2. Soma total do Valor Corrente: R$ {total_corrente:,.2f}")

# 3. Filtragem (Subconjuntos de dados)
# na=False evita erros caso existam linhas nulas na coluna
df_receitas = df[df['especificacao'].str.contains('Receita', case=False, na=False)]

# 4. Ordenação (Sorting) e Seleção de Colunas
top_5_receitas = df_receitas[['especificacao', 'valor_corrente_2024']].sort_values(
    by='valor_corrente_2024', 
    ascending=False
).head(5)

print("\n3. Top 5 Receitas (Maior para o Menor):")
print(top_5_receitas.to_string(index=False)) # to_string(index=False) remove a numeração lateral da impressão

diretorio_dados = Path(__file__).parent / 'ppa&loa'

lista_dataframes = []

for arquivo_csv in diretorio_dados.glob('*.csv'):
    print(f"Lendo o arquivo: {arquivo_csv}")
    try:
        df_temp = pd.read_csv(arquivo_csv, sep=';', encoding= 'utf-8')
        df_temp['arquivo_origem'] = arquivo_csv.name
        lista_dataframes.append(df_temp)
    except Exception as e:
        print(f"Erro ao ler {arquivo_csv.name}: {e}")

if lista_dataframes:
    df_consolidado = pd.concat(lista_dataframes, ignore_index= True)
    print("\n--- CONSOLIDAÇÃO CONCLUÍDA ---")
    print(f"Totla de linhas na nova table:{df_consolidado.shape[0]}")
    print(f"Total de colunas como resultado da união: {df_consolidado.shape[1]}")
    print(f"\nContagem de registros:")
    print(df_consolidado.columns.to_list())
else:
    print(f"Nenhum arquivo processado.")

conexao.close()