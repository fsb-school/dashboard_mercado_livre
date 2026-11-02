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


st.title("🔎 Pesquisar produtos")
st.write("Pesquise entre todos os anúncios classificados como máquinas de lavar.")

busca_produto = st.text_input(
    "Pesquisar produto",
    placeholder="Ex.: 14kg, lava e seca, branca..."
)

if not busca_produto.strip():
    st.info("Digite um termo acima para pesquisar nos títulos dos anúncios.")
else:
    resultados = df_maquinas[
        df_maquinas["eTituloProduto"].str.contains(
            busca_produto.strip(),
            case=False,
            na=False,
            regex=False
        )
    ].copy()

    resultados = resultados.sort_values(
        by=["quantidadeVendida", "numeroAvaliacoes"],
        ascending=False,
        na_position="last"
    ).reset_index(drop=True)

    st.caption(
        f"{len(resultados)} produto(s) encontrado(s) para “{busca_produto.strip()}”."
    )

    if resultados.empty:
        st.warning("Nenhum produto foi encontrado. Tente outro termo de pesquisa.")
    else:
        st.markdown("""
        <style>
        .produto-card {
            border: 1px solid #e5e5e5;
            border-top: 5px solid #FFE600;
            border-radius: 10px;
            background-color: white;
            padding: 14px;
            min-height: 430px;
            margin-bottom: 18px;
        }
        .produto-card img {
            width: 100%;
            height: 190px;
            object-fit: contain;
            margin-bottom: 12px;
        }
        .produto-titulo {
            color: #333333;
            font-size: 14px;
            line-height: 1.35;
            min-height: 58px;
            margin-bottom: 8px;
        }
        .produto-preco {
            color: #2D3277;
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 4px;
        }
        .produto-desconto {
            color: #00A650;
            font-size: 13px;
            font-weight: 600;
            min-height: 20px;
        }
        .produto-vendas {
            color: #777777;
            font-size: 13px;
            margin-top: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

        for inicio in range(0, len(resultados), 5):
            linha = resultados.iloc[inicio:inicio + 5]
            colunas = st.columns(5)

            for coluna, (_, produto) in zip(colunas, linha.iterrows()):
                preco = formatar_moeda(produto["novoPreco"])
                titulo = produto["eTituloProduto"]
                imagem = produto["imagemLink"]

                desconto = ""
                if pd.notna(produto["precoDiscount"]):
                    desconto = f'{produto["precoDiscount"]:.0f}% OFF'

                vendas = "Venda não informada"
                if pd.notna(produto["quantidadeVendida"]):
                    vendas = f'{formatar_inteiro(produto["quantidadeVendida"])} vendidos'

                with coluna:
                    st.markdown(
                        f"""
                        <div class="produto-card">
                            <img src="{imagem}">
                            <div class="produto-titulo">{titulo}</div>
                            <div class="produto-preco">{preco}</div>
                            <div class="produto-desconto">{desconto}</div>
                            <div class="produto-vendas">{vendas}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
