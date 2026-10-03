# Dados

- `raw/`: tabelas originais do [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (CC BY-NC-SA 4.0).
- `processed/`: modelo estrela gerado por `python src/etl.py`.

| Tabela | Grão | Linhas |
|---|---|---|
| `fato_vendas` | 1 item vendido | 109.880 |
| `fato_entregas` | 1 pedido entregue | 96.203 |
| `dim_cliente` | 1 cliente (id do pedido) | 99.441 |
| `dim_produto` | 1 produto | 32.951 |
| `dim_tempo` | 1 dia (jan/2017–ago/2018) | 608 |
