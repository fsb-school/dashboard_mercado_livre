import streamlit as st

st.set_page_config(
    page_title="Dashboard Mercado Livre",
    page_icon="🛒",
    layout="wide"
)

st.markdown(
    """
    <style>
    :root {
        --ml-yellow: #FFE600;
        --ml-blue: #3483FA;
        --ml-dark-blue: #2D3277;
        --ml-green: #00A650;
    }

    [data-testid="stSidebar"] {
        background-color: #f5f7fa;
    }

    h1, h2, h3 {
        color: #2D3277;
    }
    </style>
    """,
    unsafe_allow_html=True
)

dashboard_page = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="📊",
    default=True
)

produtos_page = st.Page(
    "pages/produtos.py",
    title="Produtos em destaque",
    icon="🛒"
)

frete_page = st.Page(
    "pages/frete_gratis.py",
    title="Frete grátis",
    icon="🚚"
)

todos_produtos_page = st.Page(
    "pages/todos_produtos.py",
    title="Todos os produtos",
    icon="📦"
)

pesquisar_produtos_page = st.Page(
    "pages/pesquisar_produtos.py",
    title="Pesquisar produtos",
    icon="🔎"
)

pg = st.navigation(
    [dashboard_page, produtos_page, frete_page, todos_produtos_page, pesquisar_produtos_page],
    position="hidden"
)

# Sidebar personalizada: logo grande sempre primeiro
st.sidebar.image(
    "logo_mercado_livre.png",
    width=200
)

st.sidebar.page_link(
    dashboard_page,
    label="Dashboard",
    icon="📊"
)

st.sidebar.page_link(
    produtos_page,
    label="Produtos em destaque",
    icon="🛒"
)

st.sidebar.page_link(
    frete_page,
    label="Frete grátis",
    icon="🚚"
)

st.sidebar.page_link(
    todos_produtos_page,
    label="Todos os produtos",
    icon="📦"
)

st.sidebar.page_link(
    pesquisar_produtos_page,
    label="Pesquisar produtos",
    icon="🔎"
)

st.sidebar.divider()

pg.run()
