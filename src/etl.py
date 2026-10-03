"""
ETL — Data Warehouse de vendas (Olist)

Lê as tabelas transacionais (OLTP) da Olist, trata os dados e monta um
modelo estrela (Star Schema) pronto para SQL e Power BI:

    dim_cliente ─┐
    dim_produto ─┼── fato_vendas      (1 linha por item vendido)
    dim_tempo  ──┤
                 └── fato_entregas    (1 linha por pedido entregue)

Uso:
    python src/etl.py            # gera os CSVs em data/processed/
"""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
PROCESSED = RAIZ / "data" / "processed"

# Nomes de exibição (a base original não tem acentos)
NOMES_CATEGORIAS = {
    "beleza_saude": "Beleza e saúde", "relogios_presentes": "Relógios e presentes",
    "cama_mesa_banho": "Cama, mesa e banho", "esporte_lazer": "Esporte e lazer",
    "informatica_acessorios": "Informática e acessórios", "moveis_decoracao": "Móveis e decoração",
    "utilidades_domesticas": "Utilidades domésticas", "cool_stuff": "Presentes criativos",
    "automotivo": "Automotivo", "ferramentas_jardim": "Ferramentas e jardim",
    "brinquedos": "Brinquedos", "bebes": "Bebês", "perfumaria": "Perfumaria",
    "telefonia": "Telefonia", "eletronicos": "Eletrônicos", "papelaria": "Papelaria",
    "fashion_bolsas_e_acessorios": "Moda: bolsas e acessórios", "pet_shop": "Pet shop",
    "moveis_escritorio": "Móveis de escritório", "consoles_games": "Consoles e games",
    "malas_acessorios": "Malas e acessórios", "eletroportateis": "Eletroportáteis",
    "eletrodomesticos": "Eletrodomésticos", "instrumentos_musicais": "Instrumentos musicais",
    "construcao_ferramentas_construcao": "Construção e ferramentas",
}

# Recorte de análise: meses com operação completa.
# 2016 tem apenas 267 pedidos entregues (operação inicial) e distorce as séries.
INICIO_ANALISE = "2017-01-01"
FIM_ANALISE = "2018-08-31"


def extrair() -> dict[str, pd.DataFrame]:
    """Extract — carrega as fontes OLTP."""
    datas = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    return {
        "pedidos": pd.read_csv(RAW / "olist_orders_dataset.csv", parse_dates=datas),
        "itens": pd.read_csv(RAW / "olist_order_items_dataset.csv"),
        "clientes": pd.read_csv(RAW / "olist_customers_dataset.csv"),
        "produtos": pd.read_csv(RAW / "olist_products_dataset.csv"),
        "traducao": pd.read_csv(RAW / "product_category_name_translation.csv"),
    }


def transformar(fontes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Transform — limpeza, regras de negócio e modelagem dimensional."""
    pedidos = fontes["pedidos"].drop_duplicates()
    itens = fontes["itens"].drop_duplicates()
    clientes = fontes["clientes"].drop_duplicates()
    produtos = fontes["produtos"].drop_duplicates()
    traducao = fontes["traducao"]

    # Regra de negócio: só pedidos entregues e dentro do recorte de análise
    entregues = pedidos[
        (pedidos["order_status"] == "delivered")
        & pedidos["order_purchase_timestamp"].between(INICIO_ANALISE, FIM_ANALISE + " 23:59:59")
    ].copy()
    entregues["data"] = entregues["order_purchase_timestamp"].dt.normalize()

    # ---------- Dimensão cliente ----------
    dim_cliente = (
        clientes[["customer_id", "customer_unique_id", "customer_city", "customer_state"]]
        .rename(columns={
            "customer_unique_id": "cliente_unico_id",
            "customer_city": "cidade",
            "customer_state": "uf",
        })
        .reset_index(drop=True)
    )
    dim_cliente.insert(0, "cliente_sk", dim_cliente.index + 1)

    # ---------- Dimensão produto ----------
    dim_produto = (
        produtos[["product_id", "product_category_name"]]
        .merge(traducao, on="product_category_name", how="left")
        .rename(columns={
            "product_category_name": "categoria",
            "product_category_name_english": "categoria_en",
        })
    )
    dim_produto["categoria"] = dim_produto["categoria"].fillna("sem_categoria")
    dim_produto["categoria"] = dim_produto["categoria"].map(NOMES_CATEGORIAS).fillna(
        dim_produto["categoria"].str.replace("_", " ").str.capitalize()
    )
    dim_produto["categoria_en"] = dim_produto["categoria_en"].fillna("unknown")
    dim_produto = dim_produto.reset_index(drop=True)
    dim_produto.insert(0, "produto_sk", dim_produto.index + 1)

    # ---------- Dimensão tempo (calendário contínuo, 1 linha por dia) ----------
    calendario = pd.date_range(INICIO_ANALISE, FIM_ANALISE, freq="D")
    dim_tempo = pd.DataFrame({"data": calendario})
    dim_tempo["tempo_sk"] = dim_tempo["data"].dt.strftime("%Y%m%d").astype(int)
    dim_tempo["ano"] = dim_tempo["data"].dt.year
    dim_tempo["trimestre"] = dim_tempo["data"].dt.quarter
    dim_tempo["mes"] = dim_tempo["data"].dt.month
    dim_tempo["ano_mes"] = dim_tempo["data"].dt.strftime("%Y-%m")
    dim_tempo["dia_semana"] = dim_tempo["data"].dt.dayofweek + 1  # 1 = segunda
    dim_tempo = dim_tempo[["tempo_sk", "data", "ano", "trimestre", "mes", "ano_mes", "dia_semana"]]

    chave_cliente = dim_cliente.set_index("customer_id")["cliente_sk"]
    chave_produto = dim_produto.set_index("product_id")["produto_sk"]
    entregues["tempo_sk"] = entregues["data"].dt.strftime("%Y%m%d").astype(int)
    entregues["cliente_sk"] = entregues["customer_id"].map(chave_cliente)

    # ---------- Fato vendas (grão: 1 item vendido) ----------
    fato_vendas = itens.merge(
        entregues[["order_id", "cliente_sk", "tempo_sk"]], on="order_id", how="inner"
    )
    fato_vendas["produto_sk"] = fato_vendas["product_id"].map(chave_produto)
    fato_vendas = fato_vendas.rename(columns={
        "order_id": "pedido_id",
        "order_item_id": "item_seq",
        "price": "valor_produto",
        "freight_value": "valor_frete",
    })
    fato_vendas["valor_total"] = fato_vendas["valor_produto"] + fato_vendas["valor_frete"]
    fato_vendas = fato_vendas.reset_index(drop=True)
    fato_vendas.insert(0, "venda_sk", fato_vendas.index + 1)
    fato_vendas = fato_vendas[[
        "venda_sk", "pedido_id", "item_seq", "cliente_sk", "produto_sk", "tempo_sk",
        "valor_produto", "valor_frete", "valor_total",
    ]]

    # ---------- Fato entregas (grão: 1 pedido entregue) ----------
    # Métricas de pedido ficam em fato própria para não serem somadas várias vezes
    # quando o pedido tem mais de um item.
    fato_entregas = entregues.dropna(subset=["order_delivered_customer_date"]).copy()
    fato_entregas["prazo_entrega_dias"] = (
        fato_entregas["order_delivered_customer_date"] - fato_entregas["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    fato_entregas["prazo_prometido_dias"] = (
        fato_entregas["order_estimated_delivery_date"] - fato_entregas["data"]
    ).dt.days
    fato_entregas["entregue_com_atraso"] = (
        fato_entregas["order_delivered_customer_date"].dt.normalize()
        > fato_entregas["order_estimated_delivery_date"]
    ).astype(int)
    fato_entregas = fato_entregas.rename(columns={"order_id": "pedido_id"})[[
        "pedido_id", "cliente_sk", "tempo_sk",
        "prazo_entrega_dias", "prazo_prometido_dias", "entregue_com_atraso",
    ]].round({"prazo_entrega_dias": 2})

    # ---------- Validações (integridade referencial do modelo) ----------
    assert fato_vendas["cliente_sk"].notna().all(), "venda sem cliente"
    assert fato_vendas["produto_sk"].notna().all(), "venda sem produto"
    assert fato_vendas["tempo_sk"].isin(dim_tempo["tempo_sk"]).all(), "venda fora do calendário"
    assert not fato_vendas.duplicated(["pedido_id", "item_seq"]).any(), "item duplicado"
    assert fato_entregas["pedido_id"].is_unique, "pedido duplicado na fato_entregas"

    return {
        "dim_cliente": dim_cliente,
        "dim_produto": dim_produto,
        "dim_tempo": dim_tempo,
        "fato_vendas": fato_vendas,
        "fato_entregas": fato_entregas,
    }


def carregar(modelo: dict[str, pd.DataFrame]) -> None:
    """Load — grava as tabelas do modelo estrela em CSV (prontas para o Power BI)."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for nome, tabela in modelo.items():
        tabela.to_csv(PROCESSED / f"{nome}.csv", index=False, date_format="%Y-%m-%d")


def construir_modelo() -> dict[str, pd.DataFrame]:
    return transformar(extrair())


if __name__ == "__main__":
    modelo = construir_modelo()
    carregar(modelo)
    for nome, tabela in modelo.items():
        print(f"{nome:<15} {len(tabela):>8,} linhas".replace(",", "."))
