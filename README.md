# 📊 Pipeline ETL: Dados Orçamentários Públicos

Este repositório contém um projeto prático de Engenharia de Dados focado na construção de um pipeline ETL (Extract, Transform, Load) do zero. O objetivo é processar dados financeiros brutos do planejamento orçamentário público (LDO, LOA e PPA) e estruturá-los para análise.

## 🎯 Objetivos do Projeto
- Consolidar conhecimentos fundamentais em ingestão de dados em lote (Batch Processing).
- Aplicar técnicas de Data Quality (Limpeza e Tipagem) em dados do mundo real.
- Realizar a persistência de dados em um banco de dados relacional.
- Lidar com assimetria de schema na concatenação de múltiplos arquivos.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.10+
- **Manipulação de Dados:** `pandas`
- **Banco de Dados:** `sqlite3` (Nativo)
- **Manipulação de Diretórios:** `pathlib` (Nativo)

## ⚙️ Arquitetura do Pipeline (Fluxo de Dados)

1. **Extract (Extração):**
   - Leitura automatizada em lote de múltiplos arquivos `.csv` (histórico de 2014 a 2024) localizados em um diretório específico utilizando `pathlib.Path.glob`.
   - Tratamento inicial de `encoding` (`utf-8`) e delimitadores (`seperator=';'`).
   - Implementação de rastreabilidade (adição da coluna `arquivo_origem` para identificar a fonte de cada registro).

2. **Transform (Transformação & Data Quality):**
   - Concatenação dinâmica de DataFrames (`pd.concat`), lidando automaticamente com colunas assimétricas entre os relatórios da LDO, LOA e PPA.
   - Limpeza de formatação financeira brasileira (conversão de Strings para `float64`):
     - Remoção de separadores de milhar (`.`).
     - Tratamento de valores nulos representados por hifens (`-`).
     - Conversão de valores negativos representados no padrão contábil com parênteses, ex: `(182.592)` para `-182592.0`.

3. **Load (Carga):**
   - Conexão e criação automatizada de um banco de dados SQLite (`.db`).
   - Carga inicial bruta (Raw) utilizando a biblioteca `csv` e comandos SQL puros (`INSERT INTO`).
   - Carga processada e limpa (Clean) utilizando o método `to_sql` do Pandas para persistência automatizada das tipagens corrigidas.

## 🚀 Como Executar

1. Clone este repositório.
2. Crie um ambiente virtual usando o Anaconda:
   ```bash
   conda create --name engenharia_dados python=3.10
   conda activate engenharia_dados
   conda install pandas
