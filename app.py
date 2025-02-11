import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Análise de Cancelamento de Cartões",
    page_icon="💳",
    layout="wide"
)


@st.cache_data
def load_data():
    df = pd.read_csv("dados/ClientesBanco.csv", encoding="latin1")
    df = df.drop("CLIENTNUM", axis=1)
    df = df.dropna()
    return df


df = load_data()


st.sidebar.title("Configurações")
st.sidebar.markdown("Filtros e personalizações")


categoria_selecionada = st.sidebar.selectbox(
    "Selecione a Categoria:",
    options=["Todas"] + list(df['Categoria'].unique())
)

if categoria_selecionada != "Todas":
    df = df[df['Categoria'] == categoria_selecionada]

# Título principal
st.title("Análise de Cancelamento de Cartões de Crédito")
st.markdown("**Objetivo:** Identificar padrões e motivos associados ao cancelamento")

tabs = st.tabs(["Visão Geral", "Distribuição", "Análise Detalhada", "Insights"])

with tabs[0]:
    st.header("📊 Visão Geral dos Dados")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Clientes", df.shape[0])
    with col2:
        cancelamentos = df[df['Categoria'] == 'Cancelado'].shape[0]
        st.metric("Clientes Cancelados", cancelamentos)
    with col3:
        st.metric("Taxa de Cancelamento", f"{cancelamentos/df.shape[0]*100:.2f}%")
    st.subheader("Primeiras linhas dos dados")
    st.dataframe(df.head(), use_container_width=True)

with tabs[1]:
    st.header("🔍 Análise de Distribuição")
    coluna_selecionada = st.selectbox(
        "Selecione a variável para análise:",
        df.columns.drop('Categoria')
    )
    fig = px.histogram(
        df, 
        x=coluna_selecionada, 
        color="Categoria",
        barmode='overlay', 
        nbins=50,
        title=f"Distribuição de {coluna_selecionada} por Categoria"
    )
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.header("📈 Análise Detalhada por Categoria")
    with st.expander("Ver estatísticas descritivas"):
        st.subheader("Estatísticas Descritivas")
        st.write(df.groupby('Categoria').describe().round(1).T)
    st.subheader("Análise Completa de Todas as Variáveis")
    for col in df.columns.drop('Categoria'):
        fig = px.histogram(df, x=col, color="Categoria", title=f"Distribuição de {col}")
        st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.header("💡 Principais Insights")
    st.markdown("""
    1. **Padrão de Idade:** Clientes cancelados tendem a ser mais jovens
    2. **Utilização do Cartão:** Taxas de utilização mais altas estão associadas a menor cancelamento
    3. **Interações:** Clientes com menos contatos no último ano têm maior taxa de cancelamento
    4. **Produtos Contratados:** Clientes com menos produtos tendem a cancelar mais
    """)

# Rodapé
st.markdown("---")
st.markdown("**Desenvolvido por:** [Seu Nome] | Dados: Kaggle Credit Card Customers")