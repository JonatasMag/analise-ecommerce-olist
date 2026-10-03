# Dashboard Power BI — guia de montagem

O modelo estrela já sai pronto do ETL em `data/processed/`. Este guia leva cerca de 1 hora.

## 1. Importar os dados
**Página Inicial → Obter dados → Texto/CSV** e importe os 5 arquivos de `data/processed/`:
`dim_cliente`, `dim_produto`, `dim_tempo`, `fato_vendas`, `fato_entregas`.

No Power Query, confira os tipos:
- `dim_tempo[data]` → **Data**
- colunas `valor_*` e `prazo_entrega_dias` → **Número decimal**
- colunas `*_sk` e `entregue_com_atraso` → **Número inteiro**

## 2. Relacionamentos (Exibição de modelo)
Todos **um-para-muitos**, filtro em **direção única** (dimensão → fato):

| De (1) | Para (*) |
|---|---|
| `dim_cliente[cliente_sk]` | `fato_vendas[cliente_sk]` |
| `dim_produto[produto_sk]` | `fato_vendas[produto_sk]` |
| `dim_tempo[tempo_sk]` | `fato_vendas[tempo_sk]` |
| `dim_cliente[cliente_sk]` | `fato_entregas[cliente_sk]` |
| `dim_tempo[tempo_sk]` | `fato_entregas[tempo_sk]` |

Marque `dim_tempo` como **tabela de datas** (botão direito → *Marcar como tabela de datas* → coluna `data`).

## 3. Medidas DAX
Crie uma tabela vazia chamada `_Medidas` e adicione:

```dax
Faturamento = SUM ( fato_vendas[valor_total] )

Pedidos = DISTINCTCOUNT ( fato_vendas[pedido_id] )

Ticket Médio = DIVIDE ( [Faturamento], [Pedidos] )

Clientes = DISTINCTCOUNT ( dim_cliente[cliente_unico_id] )

% Frete = DIVIDE ( SUM ( fato_vendas[valor_frete] ), [Faturamento] )

Prazo Médio (dias) = AVERAGE ( fato_entregas[prazo_entrega_dias] )

% Atraso = AVERAGE ( fato_entregas[entregue_com_atraso] )

Faturamento Mês Anterior =
    CALCULATE ( [Faturamento], DATEADD ( dim_tempo[data], -1, MONTH ) )

Variação Mensal % =
    DIVIDE ( [Faturamento] - [Faturamento Mês Anterior], [Faturamento Mês Anterior] )

Faturamento Ano Anterior =
    CALCULATE ( [Faturamento], SAMEPERIODLASTYEAR ( dim_tempo[data] ) )

% Participação UF =
    DIVIDE ( [Faturamento], CALCULATE ( [Faturamento], ALL ( dim_cliente[uf] ) ) )
```

Formate: `Faturamento` e `Ticket Médio` como moeda (R$); as medidas com `%` como porcentagem.

## 4. Páginas sugeridas

**Página 1 — Visão executiva**
- Cartões: Faturamento, Pedidos, Ticket Médio, % Atraso
- Linha: Faturamento por `dim_tempo[ano_mes]`
- Barras: Faturamento por `dim_cliente[uf]` (top 10)
- Segmentação: `dim_tempo[ano]`

**Página 2 — Logística**
- Mapa preenchido ou barras: Prazo Médio por UF, cor por % Atraso
- Colunas: % Atraso por `ano_mes` (o pico pós-Black Friday deve aparecer)
- Tabela: UF, Pedidos, Prazo Médio, % Atraso

**Página 3 — Produtos**
- Barras: Faturamento por `dim_produto[categoria]` (top 10)
- Dispersão: Ticket Médio × % Frete por UF

## 5. Conferência
Com tudo montado, os cartões sem filtro devem mostrar:
**Faturamento R$ 15.373.120 · Pedidos 96.211 · Ticket médio R$ 159,79 · % Atraso 6,8%**.
Se algum número divergir, revise os relacionamentos.

## 6. Publicar
**Arquivo → Publicar → Publicar na Web** gera um link público. Cole esse link no campo *Website* do repositório no GitHub: ele vira o botão "Ver no ar" no portfólio. Depois salve uma captura do dashboard como `reports/figures/dashboard.png`.
