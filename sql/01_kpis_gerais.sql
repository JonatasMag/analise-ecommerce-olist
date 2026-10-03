-- Visão geral do negócio no período analisado (jan/2017 a ago/2018)
SELECT
    ROUND(SUM(f.valor_total), 2)                                  AS faturamento_total,
    COUNT(DISTINCT f.pedido_id)                                   AS pedidos,
    COUNT(DISTINCT c.cliente_unico_id)                            AS clientes_unicos,
    ROUND(SUM(f.valor_total) / COUNT(DISTINCT f.pedido_id), 2)    AS ticket_medio,
    ROUND(100.0 * SUM(f.valor_frete) / SUM(f.valor_total), 1)     AS pct_frete_no_faturamento
FROM fato_vendas f
JOIN dim_cliente c ON c.cliente_sk = f.cliente_sk;
