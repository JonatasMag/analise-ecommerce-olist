# Dados para o Power BI em português

`fato_vendas.csv` traz os mesmos dados de `data/processed/fato_vendas.csv`, com os valores em **centavos** (números inteiros, sem casas decimais). Exemplo: R$ 72,19 vira `7219`.

Números inteiros são lidos da mesma forma em qualquer idioma do Power BI ou do Excel, sem a confusão entre ponto e vírgula decimal.

As medidas convertem os valores de volta para reais:

```dax
Faturamento = SUM ( fato_vendas[valor_total] ) / 100
% Frete = DIVIDE ( SUM ( fato_vendas[valor_frete] ), SUM ( fato_vendas[valor_total] ) )
```

Conferência: Faturamento R$ 15.373.120,01 · Ticket médio R$ 159,79 · Frete 14,3%.
