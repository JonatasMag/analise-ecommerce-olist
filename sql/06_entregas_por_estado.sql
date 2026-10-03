-- Desempenho logístico por estado: prazo real, prazo prometido e taxa de atraso
SELECT
    c.uf,
    COUNT(*)                                     AS pedidos_entregues,
    ROUND(AVG(e.prazo_entrega_dias), 1)          AS prazo_medio_dias,
    ROUND(AVG(e.prazo_prometido_dias), 1)        AS prazo_prometido_dias,
    ROUND(100.0 * AVG(e.entregue_com_atraso), 1) AS pct_atraso
FROM fato_entregas e
JOIN dim_cliente c ON c.cliente_sk = e.cliente_sk
GROUP BY c.uf
HAVING COUNT(*) >= 100
ORDER BY prazo_medio_dias DESC;
