-- Faturamento por estado, com participação no total e participação acumulada (Pareto)
WITH por_uf AS (
    SELECT
        c.uf,
        SUM(f.valor_total)          AS faturamento,
        COUNT(DISTINCT f.pedido_id) AS pedidos
    FROM fato_vendas f
    JOIN dim_cliente c ON c.cliente_sk = f.cliente_sk
    GROUP BY c.uf
)
SELECT
    uf,
    ROUND(faturamento, 2)                                                        AS faturamento,
    pedidos,
    ROUND(100.0 * faturamento / SUM(faturamento) OVER (), 1)                     AS pct_total,
    ROUND(100.0 * SUM(faturamento) OVER (ORDER BY faturamento DESC)
                / SUM(faturamento) OVER (), 1)                                   AS pct_acumulado
FROM por_uf
ORDER BY faturamento DESC;
