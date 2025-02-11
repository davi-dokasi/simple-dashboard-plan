import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Análise de Cancelamento de Cartões",
    page_icon="💳",
    layout="wide"
)

# Função para carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("dados/ClientesBanco.csv", encoding="latin1")
    df = df.drop("CLIENTNUM", axis=1)
    df = df.dropna()
    return df

df = load_data()

# Sidebar com filtros
st.sidebar.header("Filtros")
categoria = st.sidebar.multiselect(
    "Categoria:",
    options=df["Categoria"].unique(),
    default=df["Categoria"].unique()
)

faixa_salarial = st.sidebar.multiselect(
    "Faixa Salarial:",
    options=df["Faixa Salarial Anual"].unique(),
    default=df["Faixa Salarial Anual"].unique()
)

# Aplicar filtros
df_filtered = df.query(
    "Categoria == @categoria & `Faixa Salarial Anual` == @faixa_salarial"
)

# Página principal
st.title("🏦 Análise de Cancelamento de Cartões de Crédito")
st.markdown("##")

# Métricas principais
total_clientes = len(df_filtered)
taxa_cancelamento = round(len(df_filtered[df_filtered["Categoria"] == "Cancelado"]) / total_clientes, 2)
idade_media = df_filtered["Idade"].mean().round(1)
limite_medio = df_filtered["Limite"].mean().round(2)

left, middle, right = st.columns(3)
with left:
    st.subheader("Total de Clientes:")
    st.subheader(f"{total_clientes:,}")
with middle:
    st.subheader("Taxa de Cancelamento:")
    st.subheader(f"{taxa_cancelamento}%")
with right:
    st.subheader("Idade Média:")
    st.subheader(f"{idade_media} anos")

st.markdown("---")

# Gráficos
tab1, tab2, tab3 = st.tabs(["Distribuição Geral", "Comparativo Cancelados vs Ativos", "Análise Financeira"])

with tab1:
    st.header("Distribuição Demográfica")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(df, names="Categoria", title="Proporção de Clientes vs Cancelados")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        fig = px.histogram(df, x="Idade", nbins=20, title="Distribuição por Idade")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Comparativo entre Categorias")
    selected_column = st.selectbox(
        "Selecione a variável para análise:",
        options=["Educação", "Estado Civil", "Categoria Cartão", "Sexo"]
    )
    
    fig = px.histogram(
        df_filtered,
        x=selected_column,
        color="Categoria",
        barmode="group",
        title=f"Distribuição de {selected_column} por Categoria"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Análise Financeira")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            df_filtered,
            x="Limite",
            y="Valor Transacoes 12m",
            color="Categoria",
            title="Limite vs Valor das Transações"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        fig = px.box(
            df_filtered,
            x="Categoria",
            y="Taxa de Utilização Cartão",
            title="Taxa de Utilização do Cartão"
        )
        st.plotly_chart(fig, use_container_width=True)

# Mostrar dados brutos
st.markdown("---")
st.header("Dados Brutos")
st.dataframe(df_filtered, use_container_width=True)
st.markdown("**Desenvolvido por:** Davi Augusto Farinela da Silva | Dados: Kaggle Credit Card Customers")