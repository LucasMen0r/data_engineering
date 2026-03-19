import pandas as pd
# Carregar os dados do arquivo CSV
df = pd.read_csv('dados_clientes.csv')
# Exibir as primeiras linhas do DataFrame para verificar os dados
print(df.head(10))
# Exibir informações sobre o DataFrame
print(df.info())
# Exibir estatísticas descritivas do DataFrame
print(df.describe())
# Verificar a quantidade de valores únicos em cada coluna
print(df.nunique())
# Verificar a quantidade de valores nulos em cada coluna
print(df.isnull().sum())


def AnaliseClientes(df):
    #Análise da distribuição dos clientes por UF
    print("\nDistribuição de Clientes por UF:")
    print(df['estado'].value_counts())
    
    # Análise de distribuição de gêneros
    print("\nDistribuição de Gêneros:")
    print(df['sexo'].value_counts())
    
    #Anaálise dos stauts dos clientes
    print("\nStatus dos Clientes:")
    print(df['status'].value_counts())