import pandas as pd
import json

# Carregamento dos dados
df = pd.read_json('Aula 1/result_export2.json')

# Converter colunas de data para datetime
df['datainiciovalidade'] = pd.to_datetime(df['datainiciovalidade'])
df['datafimvalidade']    = pd.to_datetime(df['datafimvalidade'])

# Exibir informações gerais sobre o DataFrame
print("=" * 10)
print("INFORMAÇÕES GERAIS")
print("=" * 10)
print(df.info())

print("\nEstatísticas Descritivas:")
print(df.describe(include='all'))

print("\nValores Únicos por Coluna:")
print(df.nunique())

print("\nValores Nulos por Coluna:")
print(df.isnull().sum())

# Mapeamento de estados para regiões
REGIOES = {
    'Sudeste':     ['SP', 'RJ', 'MG', 'ES'],
    'Nordeste':    ['BA', 'PE', 'CE', 'MA', 'PB', 'PI', 'RN', 'AL', 'SE'],
    'Sul':         ['RS', 'SC', 'PR'],
    'Centro-Oeste':['DF', 'GO', 'MT', 'MS'],
    'Norte':       ['AM', 'PA', 'RO', 'RR', 'AC', 'AP', 'TO'],
}

def MapearRegiao(estado):
    for regiao, estados in REGIOES.items():
        if estado in estados:
            return regiao
    return 'Desconhecido'

df['regiao'] = df['estado'].map(MapearRegiao)

# Análise Geral de Clientes
def AnaliseClientes(df):
    print("\n" + "=" * 10)
    print("ANÁLISE GERAL DE CLIENTES")
    print("=" * 10)

    print("\nDistribuição por UF:")
    print(df['estado'].value_counts())

    print("\nDistribuição por Gênero:")
    print(df['sexo'].value_counts())

    print("\nStatus dos Clientes:")
    print(df['status'].value_counts())

    print("\nClientes com Validade Ativa (datafimvalidade nula):")
    ativos = df['datafimvalidade'].isna().sum()
    print(f"  Ativos:   {ativos}")
    print(f"  Inativos: {len(df) - ativos}")

# Análise de Status
def AnaliseStatus(df):
    print("\n" + "=" * 10)
    print("ANÁLISE DE STATUS")
    print("=" * 10)

    print("\nDistribuição de Status:")
    print(df['status'].value_counts())

    print("\nStatus por Gênero:")
    print(pd.crosstab(df['status'], df['sexo']))

    print("\nStatus por Região:")
    print(pd.crosstab(df['status'], df['regiao']))

# Análise por UF e Região
def AnaliseUf(df):
    print("\n" + "=" * 10)
    print("ANÁLISE POR UF E REGIÃO")
    print("=" * 10)

    print("\nClientes por UF:")
    print(df['estado'].value_counts())

    print("\nClientes por Região:")
    print(df['regiao'].value_counts())

    print("\nDetalhamento por Região e UF:")
    print(df.groupby(['regiao', 'estado']).size().rename('clientes'))

# Análise de Validade
def AnaliseValidade(df):
    """
    Substitui AnaliseVendas: como o JSON não possui coluna 'vendas',
    esta função analisa as datas de início e fim de validade dos clientes.
    """
    print("\n" + "=" * 10)
    print("ANÁLISE DE VALIDADE")
    print("=" * 10)

    print("\nData de Início de Validade — Estatísticas:")
    print(df['datainiciovalidade'].describe())

    clientes_inativos = df.dropna(subset=['datafimvalidade'])
    print(f"\nClientes com data fim preenchida (inativos): {len(clientes_inativos)}")

    if not clientes_inativos.empty:
        clientes_inativos = clientes_inativos.copy()
        clientes_inativos['duracao_dias'] = (
            clientes_inativos['datafimvalidade'] - clientes_inativos['datainiciovalidade']
        ).dt.days
        print("\nDuração de Validade (dias) — Estatísticas:")
        print(clientes_inativos['duracao_dias'].describe())

    print("\nInício de Validade por Status:")
    print(df.groupby('status')['datainiciovalidade'].agg(['min', 'max', 'count']))

# Execução de todas as análises

if __name__ == '__main__':
    AnaliseClientes(df)
    AnaliseStatus(df)
    AnaliseUf(df)
    AnaliseValidade(df)