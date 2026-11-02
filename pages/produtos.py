import streamlit as st
import pandas as pd


def formatar_moeda(valor):
    valor_formatado = f"{valor:,.2f}"
    valor_formatado = valor_formatado.replace(",", "X")
    valor_formatado = valor_formatado.replace(".", ",")
    valor_formatado = valor_formatado.replace("X", ".")
    return f"R$ {valor_formatado}"


def formatar_inteiro(valor):
    return f"{valor:,.0f}".replace(",", ".")


@st.cache_data
def carregar_dados():
    df = pd.read_csv("dataset_mercadolivre-scraper.csv")
    df = df.dropna(axis=1, how="all")

    df["novoPreco"] = df["novoPreco"].str.replace(",", ".", regex=False)
    df["novoPreco"] = pd.to_numeric(df["novoPreco"], errors="coerce")

    df["precoAnterior"] = df["precoAnterior"].str.replace(",", ".", regex=False)
    df["precoAnterior"] = pd.to_numeric(df["precoAnterior"], errors="coerce")

    df["precoDiscount"] = df["precoDiscount"].str.replace(
        "% OFF", "", regex=False
    )
    df["precoDiscount"] = pd.to_numeric(
        df["precoDiscount"], errors="coerce"
    )

    palavras_pecas = [
        "parafuso", "capacitor", "suporte", "selo",
        "válvula", "valvula", "rede elétrica", "rede eletrica",
        "atuador", "cinta", "chave seletora",
        "chicote", "gabinete"
    ]

    palavras_maquinas = [
        "máquina de lavar", "maquina de lavar",
        "máquina lavar", "maquina lavar",
        "máquina electrolux", "maquina electrolux",
        "lavadora", "lavaroupas", "lava roupas",
        "lava roupa", "lava e seca", "top load"
    ]

    padrao_maquinas = "|".join(palavras_maquinas)
    padrao_pecas = "|".join(palavras_pecas)

    tem_maquina = df["eTituloProduto"].str.contains(
        padrao_maquinas, case=False, na=False
    )
    tem_peca = df["eTituloProduto"].str.contains(
        padrao_pecas, case=False, na=False
    )

    df["tipoProduto"] = "Revisar"
    df.loc[tem_maquina & ~tem_peca, "tipoProduto"] = "Máquina"
    df.loc[tem_peca, "tipoProduto"] = "Peça/Acessório"

    df.loc[[200, 205, 210, 229], "tipoProduto"] = "Máquina"

    df_maquinas = df[
        df["tipoProduto"] == "Máquina"
    ].copy()

    return df_maquinas


df_maquinas = carregar_dados()


st.markdown(
    """
    <style>
    h1, h2, h3 {
        color: #2D3277;
    }

    .produto-card {
        border-top: 5px solid #FFE600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛒 Produtos em destaque")

st.write(
    "Os 10 anúncios com maior volume de vendas entre as máquinas analisadas."
)

st.caption(
    "Produtos ordenados pela quantidade vendida e, em caso de empate, "
    "pelo número de avaliações."
)

produtos_destaque = (
    df_maquinas
    .dropna(subset=["quantidadeVendida"])
    .sort_values(
        by=["quantidadeVendida", "numeroAvaliacoes"],
        ascending=False
    )
    .head(10)
    .reset_index(drop=True)
)

if produtos_destaque.empty:
    st.info(
        "Nenhum produto com informação de vendas foi encontrado."
    )
else:
    st.markdown(
        """
        <style>
        .produto-card {
            background-color: white;
            border: 1px solid #e5e5e5;
            border-radius: 8px;
            padding: 12px;
            height: 500px;
            display: flex;
            flex-direction: column;
            box-sizing: border-box;
        }

        .produto-imagem {
            width: 100%;
            height: 220px;
            object-fit: contain;
            display: block;
            margin-bottom: 12px;
        }

        .produto-titulo {
            font-size: 15px;
            line-height: 1.35;
            height: 61px;
            margin-bottom: 10px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .produto-preco {
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .produto-desconto {
            color: #00a650;
            font-size: 14px;
            height: 21px;
            margin-bottom: 6px;
        }

        .produto-vendas {
            color: #666666;
            font-size: 14px;
            margin-top: auto;
        }

        .espaco-linha {
            margin-bottom: 22px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    for inicio in range(0, len(produtos_destaque), 5):
        produtos_linha = produtos_destaque.iloc[
            inicio:inicio + 5
        ]

        colunas = st.columns(5)

        for coluna, (_, produto) in zip(
            colunas,
            produtos_linha.iterrows()
        ):
            if pd.notna(produto["precoDiscount"]):
                desconto = f'{produto["precoDiscount"]:.0f}% OFF'
            else:
                desconto = "&nbsp;"

            card_html = (
                '<div class="produto-card">'
                f'<img src="{produto["imagemLink"]}" '
                'class="produto-imagem" alt="Imagem do produto">'
                f'<div class="produto-titulo">'
                f'{produto["eTituloProduto"]}</div>'
                f'<div class="produto-preco">'
                f'{formatar_moeda(produto["novoPreco"])}</div>'
                f'<div class="produto-desconto">'
                f'{desconto}</div>'
                f'<div class="produto-vendas">'
                f'{formatar_inteiro(produto["quantidadeVendida"])} '
                'vendidos</div>'
                '</div>'
            )

            with coluna:
                st.markdown(
                    card_html,
                    unsafe_allow_html=True
                )

        st.markdown(
            '<div class="espaco-linha"></div>',
            unsafe_allow_html=True
        )
