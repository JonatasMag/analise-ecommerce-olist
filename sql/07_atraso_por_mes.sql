-- Taxa de atraso ao longo do tempo: a operação aguentou os picos de demanda?
SELECT
    t.ano_mes,
    COUNT(*)                                     AS pedidos_entregues,
    ROUND(100.0 * AVG(e.entregue_com_atraso), 1) AS pct_atraso,
    ROUND(AVG(e.prazo_entrega_dias), 1)          AS prazo_medio_dias
FROM fato_entregas e
JOIN dim_tempo t ON t.tempo_sk = e.tempo_sk
GROUP BY t.ano_mes
ORDER BY t.ano_mes;
