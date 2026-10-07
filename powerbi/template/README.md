# Modelos visuais do dashboard

Três imagens de fundo (1920 × 1080), uma por página, mais um **tema** de cores. Elas já trazem o cabeçalho, os títulos, os subtítulos com as conclusões e as molduras brancas. Os gráficos do Power BI ficam transparentes, por cima de cada moldura.

| Arquivo | Página |
|---|---|
| `01_visao_executiva.png` | Visão Executiva |
| `02_logistica.png` | Logística |
| `03_produtos.png` | Produtos |
| `tema_olist.json` | Cores e fundo transparente para todos os gráficos |

## Passo 1: aplicar o tema (uma vez só)
**Exibição → Temas** (clique na setinha da galeria) → **Procurar temas** → escolha `tema_olist.json`.

Todos os gráficos ficam com fundo transparente, sem borda, sem título próprio e com as cores do portfólio.

## Passo 2: colocar a imagem de fundo (em cada página)
1. Clique num **espaço vazio** da página.
2. No painel **Visualizações**, clique no **pincel** (*Formatar sua página*).
3. Abra **Plano de fundo da tela**:
   - **Imagem → Procurar** → escolha a imagem da página;
   - **Ajuste da imagem:** *Ajustar*;
   - **Transparência:** **0%**.

## Passo 3: apagar os textos antigos do topo
O título e o subtítulo já estão na imagem. Apague as caixas de texto antigas ("VISÃO EXECUTIVA", "/ Olist – E-comerce").

## Passo 4: encaixar cada gráfico na moldura
Clique no gráfico → **pincel** → **Geral → Propriedades → Tamanho e Posição** e digite os números:

| Página | Gráfico | Horizontal (X) | Vertical (Y) | Largura | Altura |
|---|---|---|---|---|---|
| Visão Executiva | Cartão Faturamento | 40 | 128 | 357 | 126 |
| Visão Executiva | Cartão Pedidos | 513 | 128 | 357 | 126 |
| Visão Executiva | Cartão Ticket médio | 986 | 128 | 357 | 126 |
| Visão Executiva | Cartão % de atraso | 1459 | 128 | 357 | 126 |
| Visão Executiva | Segmentação de ano | 224 | 298 | 720 | 86 |
| Visão Executiva | Faturamento mensal | 36 | 488 | 912 | 556 |
| Visão Executiva | Faturamento por estado | 992 | 358 | 892 | 686 |
| Logística | Prazo por estado | 36 | 188 | 1406 | 376 |
| Logística | Atraso por mês | 36 | 668 | 1406 | 376 |
| Logística | Tabela de prazos | 1486 | 188 | 398 | 856 |
| Produtos | Categorias | 36 | 188 | 912 | 856 |
| Produtos | Ticket x frete | 992 | 188 | 892 | 856 |

Na tabela de prazos, desligue o título próprio (**Geral → Título → Desativado**): o título já está na imagem.

## Opcional: botões de navegação
As abas do cabeçalho (1 Visão Executiva · 2 Logística · 3 Produtos) são desenho. Para torná-las clicáveis, use **Inserir → Botões → Em branco**, coloque o botão em cima de cada aba e, em **Ação**, escolha **Tipo: Navegação de página** e a página de destino.
