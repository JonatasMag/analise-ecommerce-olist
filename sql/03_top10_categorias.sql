-- 10 categorias com maior faturamento
SELECT
    p.categoria,
    ROUND(SUM(f.valor_total), 2)                                         AS faturamento,
    COUNT(*)                                                             AS itens_vendidos,
    ROUND(AVG(f.valor_produto), 2)                                       AS preco_medio,
    ROUND(100.0 * SUM(f.valor_total) / (SELECT SUM(valor_total) FROM fato_vendas), 1) AS pct_total
FROM fato_vendas f
JOIN dim_produto p ON p.produto_sk = f.produto_sk
GROUP BY p.categoria
ORDER BY faturamento DESC
LIMIT 10;
