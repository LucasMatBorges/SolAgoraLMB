-- Países com mais transações
SELECT 
    country,
    COUNT(*) AS total_transactions
FROM solagora.transactions_country
GROUP BY country
ORDER BY total_transactions DESC;

-- Bancos com mais transações
SELECT 
    bank,
    COUNT(*) AS total_transactions
FROM solagora.transactions_country
GROUP BY bank
ORDER BY total_transactions DESC;

-- Datas com mais transações
SELECT 
    transaction_date,
    COUNT(*) AS total_transactions
FROM solagora.transactions_country
GROUP BY transaction_date
ORDER BY total_transactions DESC;

-- Pagamentos de transações mais atrasados
SELECT
    transaction_id,
    country,
    bank,
    company,
    transaction_date,
    payment_due_date,
    days_delay
FROM solagora.transactions_country
WHERE is_late = true
ORDER BY days_delay DESC
LIMIT 100;
