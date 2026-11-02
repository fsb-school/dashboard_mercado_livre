import streamlit as st
import pandas as pd
import plotly.express as px


def formatar_moeda(valor):
    valor_formatado = f"{valor:,.2f}"
    valor_formatado = valor_formatado.replace(",", "X")
    valor_formatado = valor_formatado.replace(".", ",")
    valor_formatado = valor_formatado.replace("X", ".")
    return f"R$ {valor_formatado}"


def formatar_inteiro(valor):
    return f"{valor:,.0f}".replace(",", ".")


st.markdown("""
<style>
.top-insight {
    background-color: #FFF9D6;
    border: 1px solid #FFE600;
    border-radius: 12px;
    padding: 22px 26px;
    margin-top: 8px;
}

.top-insight-text {
    color: #2D3277;
    font-size: 17px;
    font-style: italic;
    line-height: 1.5;
}

.top-insight-line {
    width: 45px;
    height: 3px;
    background-color: #3483FA;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

col_titulo, col_insight = st.columns(
    [2.2, 1],
    gap="large"
)

with col_titulo:
    st.title("🛒 Dashboard de Produtos do Mercado Livre")
    st.write(
        "Análise interativa de anúncios de máquinas de lavar Electrolux."
    )

with col_insight:
    st.markdown(
        '<div class="top-insight">'
        '<div class="top-insight-text">'
        '💡 &nbsp;“Anúncios com maiores descontos apresentam tendência de maior quantidade vendida.”'
        '</div>'
        '<div class="top-insight-line"></div>'
        '</div>',
        unsafe_allow_html=True
    )


@st.cache_data
def carregar_dados():

    df = pd.read_csv("dataset_mercadolivre-scraper.csv")

    # Remove colunas completamente vazias
    df = df.dropna(axis=1, how="all")

    # Converte o preço atual para formato numérico
    df["novoPreco"] = df["novoPreco"].str.replace(
        ",",
        ".",
        regex=False
    )

    df["novoPreco"] = pd.to_numeric(
        df["novoPreco"],
        errors="coerce"
    )

    df["precoAnterior"] = df["precoAnterior"].str.replace(
        ",",
        ".",
        regex=False
    )

    df["precoAnterior"] = pd.to_numeric(
        df["precoAnterior"],
        errors="coerce"
    )

    df["precoDiscount"] = df["precoDiscount"].str.replace(
        "% OFF",
        "",
        regex=False
    )

    df["precoDiscount"] = pd.to_numeric(
        df["precoDiscount"],
        errors="coerce"
    )

    # Palavras utilizadas para identificar peças e acessórios
    palavras_pecas = [
        "parafuso",
        "capacitor",
        "suporte",
        "selo",
        "válvula",
        "valvula",
        "rede elétrica",
        "rede eletrica",
        "atuador",
        "cinta",
        "chave seletora",
        "chicote",
        "gabinete"
    ]

    # Palavras utilizadas para identificar máquinas
    palavras_maquinas = [
        "máquina de lavar",
        "maquina de lavar",
        "máquina lavar",
        "maquina lavar",
        "máquina electrolux",
        "maquina electrolux",
        "lavadora",
        "lavaroupas",
        "lava roupas",
        "lava roupa",
        "lava e seca",
        "top load"
    ]


    padrao_maquinas = "|".join(palavras_maquinas)
    padrao_pecas = "|".join(palavras_pecas)

    tem_maquina = df["eTituloProduto"].str.contains(
        padrao_maquinas,
        case=False,
        na=False
    )

    tem_peca = df["eTituloProduto"].str.contains(
        padrao_pecas,
        case=False,
        na=False
    )

    df["tipoProduto"] = "Revisar"

    df.loc[
        tem_maquina & ~tem_peca,
        "tipoProduto"
    ] = "Máquina"

    df.loc[
        tem_peca,
        "tipoProduto"
    ] = "Peça/Acessório"

    df.loc[
        [200, 205, 210, 229],
        "tipoProduto"
    ] = "Máquina"

    df_maquinas = df[
        df["tipoProduto"] == "Máquina"
    ].copy()

    return df_maquinas

df_maquinas = carregar_dados()

# Quantidade de máquinas anunciadas com frete grátis
total_frete_gratis = int(
    df_maquinas["freteGratis"].fillna(False).eq(True).sum()
)


# CARDS

st.markdown(
    """
    <style>
    .nav-card {
        border: 1px solid #d9d9d9;
        border-radius: 10px;
        padding: 20px 22px 70px 22px;
        min-height: 205px;
        margin: 12px 0 -58px 0;
    }

    .nav-card-produtos {
        border-left: 7px solid #FFE600;
        background: linear-gradient(90deg, #fffbea 0%, #ffffff 55%);
    }

    .nav-card-frete {
        border-left: 7px solid #3483FA;
        background: linear-gradient(90deg, #eef6ff 0%, #ffffff 55%);
    }

    .nav-card-icon {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        margin-bottom: 10px;
    }

    .nav-card-icon-produtos {
        background-color: #FFE600;
    }

    .nav-card-icon-frete {
        background-color: #DDEBFF;
    }

    .nav-card-title {
        color: #2D3277;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .nav-card-number {
        color: #2D3277;
        font-size: 29px;
        font-weight: 500;
        margin-bottom: 5px;
    }

    .nav-card-text {
        color: #777777;
        font-size: 14px;
    }

    div[data-testid="stButton"] > button {
        width: auto;
        background-color: #3483FA;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 20px;
        margin-left: 22px;
    }

    div[data-testid="stButton"] > button:hover {
        background-color: #2968C8;
        color: white;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

card_produtos, card_frete, card_pesquisa = st.columns(3, gap="medium")

with card_produtos:
    st.markdown(
        """
        <div class="nav-card nav-card-produtos">
            <div class="nav-card-icon nav-card-icon-produtos">🛒</div>
            <div class="nav-card-title">Produtos em destaque</div>
            <div class="nav-card-number">10 produtos</div>
            <div class="nav-card-text">
                Conheça os anúncios com maior volume de vendas.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Ver produtos →",
        key="ver_produtos"
    ):
        st.switch_page("pages/produtos.py")

with card_frete:
    st.markdown(
        f"""
        <div class="nav-card nav-card-frete">
            <div class="nav-card-icon nav-card-icon-frete">🚚</div>
            <div class="nav-card-title">Frete grátis</div>
            <div class="nav-card-number">{formatar_inteiro(total_frete_gratis)} anúncios</div>
            <div class="nav-card-text">
                Explore máquinas anunciadas com frete grátis.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Ver anúncios →",
        key="ver_frete_gratis"
    ):
        st.switch_page("pages/frete_gratis.py")


with card_pesquisa:
    st.markdown(
        """
        <div class="nav-card nav-card-produtos">
            <div class="nav-card-icon nav-card-icon-frete">🔎</div>
            <div class="nav-card-title">Pesquisar produtos</div>
            <div class="nav-card-number">Busca</div>
            <div class="nav-card-text">
                Encontre máquinas pelo nome ou característica do anúncio.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Pesquisar →",
        key="pesquisar_produtos"
    ):
        st.switch_page("pages/pesquisar_produtos.py")


df_resumo = df_maquinas[
    df_maquinas["novoPreco"] < 1500000
].copy()

total_anuncios = len(df_resumo)
preco_mediano = df_resumo["novoPreco"].median()
desconto_mediano = df_resumo["precoDiscount"].median()
maior_venda = df_resumo["quantidadeVendida"].max()

st.subheader("Visão geral")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Máquinas anunciadas",
    formatar_inteiro(total_anuncios)
)

col2.metric(
    "Preço mediano",
    formatar_moeda(preco_mediano)
)

col3.metric(
    "Desconto mediano",
    f"{desconto_mediano:.0f}%"
)

col4.metric(
    "Maior volume de vendas",
    formatar_inteiro(maior_venda)
)

st.subheader("Análise dos anúncios")


# GRÁFICO 1 

st.subheader("Desconto × Quantidade Vendida")

df_grafico1 = df_resumo.dropna(
    subset=["precoDiscount", "quantidadeVendida"]
).copy()

correlacao_desconto = df_grafico1[
    ["precoDiscount", "quantidadeVendida"]
].corr().iloc[0, 1]

correlacao_formatada = f"{correlacao_desconto:.2f}".replace(".", ",")

st.caption(
    f"Correlação entre desconto e quantidade vendida: {correlacao_formatada}"
)

fig_desconto = px.scatter(
    df_grafico1,
    x="precoDiscount",
    y="quantidadeVendida",
    hover_name="eTituloProduto",
    hover_data={
        "novoPreco": True,
        "numeroAvaliacoes": True,
        "precoDiscount": False,
        "quantidadeVendida": False
    },
    labels={
        "precoDiscount": "Desconto (%)",
        "quantidadeVendida": "Quantidade vendida",
        "novoPreco": "Preço (R$)",
        "numeroAvaliacoes": "Número de avaliações"
    },
    trendline="ols"
)

fig_desconto.update_traces(
    marker=dict(
        size=10,
        color="#3483FA",
        opacity=0.65
    )
)

fig_desconto.update_layout(
    height=500,
    plot_bgcolor="white",
    title=None
)

st.plotly_chart(
    fig_desconto,
    use_container_width=True
)


st.markdown("""
<style>
.insight-card {
    background-color: #FFF9D6;
    border: 1px solid #FFE600;
    border-radius: 12px;
    padding: 24px 28px;
    margin-top: 18px;
    margin-bottom: 30px;
}

.insight-text {
    color: #2D3277;
    font-size: 17px;
    font-style: italic;
    line-height: 1.5;
}

.insight-line {
    width: 48px;
    height: 3px;
    background-color: #3483FA;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

# GRÁFICO 2

st.subheader("Quantidade Vendida × Número de Avaliações")

df_grafico2 = df_resumo.dropna(
    subset=["quantidadeVendida", "numeroAvaliacoes"]
).copy()

# Calcula a correlação usando os anúncios individuais.
correlacao_avaliacoes = df_grafico2[
    ["quantidadeVendida", "numeroAvaliacoes"]
].corr().iloc[0, 1]

correlacao_avaliacoes_formatada = (
    f"{correlacao_avaliacoes:.2f}".replace(".", ",")
)

st.caption(
    "Produtos com maior quantidade vendida também tendem a ter mais avaliações? "
    f"Correlação: {correlacao_avaliacoes_formatada}"
)


df_mediana_avaliacoes = (
    df_grafico2
    .groupby("quantidadeVendida", as_index=False)["numeroAvaliacoes"]
    .median()
    .sort_values("quantidadeVendida")
)


df_mediana_avaliacoes["faixa_vendas"] = (
    df_mediana_avaliacoes["quantidadeVendida"]
    .apply(lambda x: formatar_inteiro(x))
)

fig_avaliacoes = px.line(
    df_mediana_avaliacoes,
    x="faixa_vendas",
    y="numeroAvaliacoes",
    markers=True,
    labels={
        "faixa_vendas": "Quantidade vendida",
        "numeroAvaliacoes": "Mediana do número de avaliações"
    }
)

fig_avaliacoes.update_traces(
    line=dict(
        color="#3483FA",
        width=3
    ),
    marker=dict(
        size=10,
        color="#FFE600",
        line=dict(
            color="#2D3277",
            width=1.5
        )
    )
)


faixas_anotadas = {1000, 5000, 10000}

for posicao, (_, linha) in enumerate(df_mediana_avaliacoes.iterrows()):
    if linha["quantidadeVendida"] in faixas_anotadas:
        fig_avaliacoes.add_annotation(
            x=posicao,
            y=linha["numeroAvaliacoes"],
            xref="x",
            yref="y",
            text=f"<b>{formatar_inteiro(linha['numeroAvaliacoes'])}</b>",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#3483FA",
            arrowsize=1,
            arrowwidth=1.5,
            ax=0,
            ay=-38,
            bgcolor="white",
            bordercolor="#3483FA",
            borderwidth=1,
            borderpad=5,
            font=dict(
                color="#2D3277",
                size=12
            )
        )

fig_avaliacoes.add_annotation(
    xref="paper",
    yref="paper",
    x=0.03,
    y=0.95,
    text=(
        f"<b>Correlação: {correlacao_avaliacoes_formatada}</b><br>"
        "Forte associação positiva"
    ),
    showarrow=False,
    align="left",
    bgcolor="#EEF6FF",
    bordercolor="#3483FA",
    borderwidth=1,
    borderpad=7,
    font=dict(
        color="#2D3277",
        size=12
    )
)

fig_avaliacoes.update_layout(
    height=520,
    plot_bgcolor="white",
    title=None,
    xaxis=dict(
        type="category",
        categoryorder="array",
        categoryarray=df_mediana_avaliacoes["faixa_vendas"].tolist()
    ),
    yaxis=dict(
        rangemode="tozero"
    ),
    margin=dict(
        t=60,
        r=30,
        b=40,
        l=40
    )
)

fig_avaliacoes.update_xaxes(
    showgrid=False
)

fig_avaliacoes.update_yaxes(
    gridcolor="#EEEEEE"
)

st.plotly_chart(
    fig_avaliacoes,
    use_container_width=True
)

st.markdown(
    '<div class="insight-card">'
    '<div class="insight-text">'
    '💡 &nbsp;&nbsp;“Anúncios com maior volume de vendas apresentam tendência '
    'de possuir também maior número de avaliações.”'
    '</div>'
    '<div class="insight-line"></div>'
    '</div>',
    unsafe_allow_html=True
)

