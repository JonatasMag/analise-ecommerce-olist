-- Ticket médio por estado (somente estados com amostra relevante: 500+ pedidos)
-- O ticket é calculado por PEDIDO, não por item, para não distorcer pedidos com vários itens.
WITH pedidos AS (
    SELECT
        f.pedido_id,
        c.uf,
        SUM(f.valor_total) AS valor_pedido,
        SUM(f.valor_frete) AS frete_pedido
    FROM fato_vendas f
    JOIN dim_cliente c ON c.cliente_sk = f.cliente_sk
    GROUP BY f.pedido_id, c.uf
)
SELECT
    uf,
    COUNT(*)                                            AS pedidos,
    ROUND(AVG(valor_pedido), 2)                         AS ticket_medio,
    ROUND(AVG(frete_pedido), 2)                         AS frete_medio,
    ROUND(100.0 * SUM(frete_pedido) / SUM(valor_pedido), 1) AS pct_frete
FROM pedidos
GROUP BY uf
HAVING COUNT(*) >= 500
ORDER BY ticket_medio DESC;
