-- Evolução mensal do faturamento, com variação contra o mês anterior
WITH mensal AS (
    SELECT
        t.ano_mes,
        SUM(f.valor_total)          AS faturamento,
        COUNT(DISTINCT f.pedido_id) AS pedidos
    FROM fato_vendas f
    JOIN dim_tempo t ON t.tempo_sk = f.tempo_sk
    GROUP BY t.ano_mes
)
SELECT
    ano_mes,
    ROUND(faturamento, 2) AS faturamento,
    pedidos,
    ROUND(faturamento / pedidos, 2) AS ticket_medio,
    ROUND(100.0 * (faturamento - LAG(faturamento) OVER (ORDER BY ano_mes))
                / LAG(faturamento) OVER (ORDER BY ano_mes), 1) AS variacao_mes_pct
FROM mensal
ORDER BY ano_mes;
