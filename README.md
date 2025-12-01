# 🚀 Pipeline de Dados em AWS

Este projeto cria um pipeline simples de dados utilizando serviços serverless da AWS para processar arquivos CSV de transações e enriquecê-los com informações de países.  
O objetivo é gerar uma tabela final pronta para análises usando Amazon Athena.

---

# 📁 Arquitetura do Projeto

O pipeline é composto por:

1. **S3 – Data Lake (Bronze e Gold)**
2. **Glue Job – Limpeza, Enriquecimento e Processamento**
3. **Athena – Tabela Final e Consultas**

A seguir está uma explicação simples e direta de cada componente.

---

# 🪣 1. S3 – Organização do Data Lake

O bucket do projeto é:

```
solagoralmb
```

Estrutura utilizada:

```
solagoralmb/
  ├─ bronze/
  │    ├─ countries/
  │    │     └─ countries.csv
  │    └─ transactions/
  │          └─ transactions_*.csv
  │
  └─ gold/
       └─ transactions_country/
```

### • Bronze  
Armazena os arquivos CSV brutos exatamente como foram recebidos.

### • Gold  
Armazena os dados já tratados, enriquecidos e convertidos para **Parquet**, prontos para uso no Athena.

---

# 🚀 2. Glue Job – ETL (PySpark)

O Glue Job é responsável por:

- Ler os CSV brutos da camada Bronze
- Tratar tipos (datas, números)
- Enriquecer os dados com a tabela de países
- Calcular:
  - `days_delay`
  - `is_late`
- Escrever o resultado final na camada Gold, em Parquet

Script utilizado no Glue:

```
src/glue/transactions_etl.py
```

A saída do job é gravada em:

```
s3://solagoralmb/gold/transactions_country/
```

---

# 📊 3. Athena – Tabela Final

Após o Glue Job gerar os arquivos Parquet, criamos a tabela no Athena:

```sql
CREATE DATABASE IF NOT EXISTS finance;

CREATE EXTERNAL TABLE IF NOT EXISTS finance.transactions_country (
  transaction_id        string,
  country_code          string,
 country               string,
  transaction_date      date,
  bank                  string,
  company               string,
  transaction_value     double,
  payment_due_date      date,
  days_delay            int,
  is_late               boolean
)
PARTITIONED BY (
  ingestion_date string
)
STORED AS PARQUET
LOCATION 's3://solagoralmb/gold/transactions_country/';
```

Atualizar as partições:

```sql
MSCK REPAIR TABLE finance.transactions_country;
```

---

# 📈 Consultas de Negócio (Athena)

### Países com mais transações
```sql
SELECT country, COUNT(*) AS total
FROM finance.transactions_country
GROUP BY country
ORDER BY total DESC;
```

### Bancos com mais transações
```sql
SELECT bank, COUNT(*) AS total
FROM finance.transactions_country
GROUP BY bank
ORDER BY total DESC;
```

### Datas com maior volume
```sql
SELECT transaction_date, COUNT(*) AS total
FROM finance.transactions_country
GROUP BY transaction_date
ORDER BY total DESC;
```

### Transações mais atrasadas
```sql
SELECT *
FROM finance.transactions_country
WHERE is_late = true
ORDER BY days_delay DESC
LIMIT 50;
```

---

# 📦 Estrutura do Repositório

```
.
├── README.md
│
├── src/
│    └── glue/
│          └── transactions_etl.py
│
└── athena/
     ├── create_table.sql
     └── queries.sql
```

---

# 🛠️ Como Executar

1. Suba os CSV de países e transações para o S3 na pasta **bronze/**
2. Rode o Glue Job usando o script `transactions_etl.py`
3. Verifique se os Parquets foram gerados na pasta **gold/**
4. Crie a tabela no Athena
5. Execute as consultas de negócio

---

# 🎯 Resultado Final

No fim, o pipeline entrega:

- Dados brutos armazenados no S3 (Bronze)
- Dados tratados e enriquecidos em Parquet (Gold)
- Tabela final no Athena pronta para consultas
- SQLs para análise de países, bancos, datas e atrasos

Pipeline simples, direto ao ponto e funcional usando componentes totalmente serverless da AWS.
