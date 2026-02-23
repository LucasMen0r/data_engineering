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
# ETL Pipeline: Public Budget Data

This repository contains a practical Data Engineering project focused on building an ETL (Extract, Transform, Load) pipeline from scratch. The main goal is to process raw public financial and budget planning data (LDO, LOA, and PPA reports) and structure them for analytical consumption.

## Objectives
- Consolidate foundational knowledge in Batch Processing and data ingestion.
- Apply Data Quality techniques (cleaning, casting, and standardizing) to real-world data.
- Persist structured data into a relational database.
- Handle schema asymmetry when concatenating multiple files from different sources.

## Tech Stack
- **Language:** Python 3.10+
- **Data Manipulation:** `pandas`
- **Database:** `sqlite3` (Built-in)
- **Path Management:** `pathlib` (Built-in)

## Pipeline Architecture

1. **Extract:**
   - Automated batch reading of multiple `.csv` files (historical data from 2014 to 2024) located in a target directory using `pathlib.Path.glob`.
   - Initial handling of distinct `encoding` (`utf-8`) and delimiters (`separator=';'`).
   - Implementation of data traceability by appending an `arquivo_origem` (source file) column to identify the origin of each parsed row.

2. **Transform (Data Quality):**
   - Dynamic DataFrame concatenation (`pd.concat`), automatically handling asymmetric columns across the LDO, LOA, and PPA reports.
   - Cleansing of Brazilian financial formatting (converting Strings to `float64`):
     - Removal of thousand separators (`.`).
     - Handling of null values represented by accounting hyphens (`-`).
     - Parsing negative values formatted in accounting standard with parentheses (e.g., converting `(182.592)` to `-182592.0`).

3. **Load:**
   - Automated connection and schema creation in an SQLite database (`.db`).
   - Initial Raw load utilizing the built-in `csv` library and native SQL statements (`INSERT INTO`).
   - Clean load utilizing the pandas `to_sql` method for automated persistence with corrected data typing.

## How to Run

1. Clone this repository.
2. Create a virtual environment using Anaconda:
   ```bash
   conda create --name data_engineering python=3.10
   conda activate data_engineering
   conda install pandas
