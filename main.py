import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÕES DA PÁGINA E DESIGN
st.set_page_config(
    page_title="FarmaStock | Inteligência de Dados",
    page_icon="💊",
    layout="wide"
)

# Cores Corporativas
COLOR_PRIMARY = "#004a99"
COLOR_BACKGROUND = "#f8f9fa"

# Injeção de CSS para um visual Premium
st.markdown(f"""
    <style>
    .main {{ background-color: {COLOR_BACKGROUND}; }}
    .stMetric {{
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e1f5fe;
    }}
    h1, h2, h3 {{ color: {COLOR_PRIMARY}; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
    </style>
    """, unsafe_allow_html=True)

# 2. CARREGAMENTO DE DADOS (Simulado - Substituível por seu SQL)
@st.cache_data
def load_data():
    data = {
        'Produto': ['Amoxicilina', 'Dipirona', 'Paracetamol', 'Omeprazol', 'Ibuprofeno', 'Loratadina', 'Vitamina C'],
        'Categoria': ['Antibiótico', 'Analgésico', 'Analgésico', 'Gastro', 'Anti-inflamatório', 'Antialérgico', 'Suplemento'],
        'Estoque': [5, 85, 12, 8, 50, 4, 30],
        'Estoque_Minimo': [10, 20, 15, 10, 15, 10, 10],
        'Preco_Venda': [45.90, 12.50, 18.00, 32.40, 22.00, 15.90, 25.00],
        'Vendas_Mes': [120, 340, 210, 95, 150, 80, 200]
    }
    df = pd.DataFrame(data)
    df['Status'] = df.apply(lambda x: '🚨 Repor' if x['Estoque'] < x['Estoque_Minimo'] else '✅ OK', axis=1)
    df['Total_Vendas_RS'] = df['Vendas_Mes'] * df['Preco_Venda']
    return df

df = load_data()

# 3. SIDEBAR (FILTROS E BRANDING)
with st.sidebar:
    st.markdown(f"<h2 style='text-align: center;'>FarmaStock</h2>", unsafe_allow_html=True)
    st.divider()
    st.subheader("Filtros de Visão")
    categorias = st.multiselect("Categorias:", options=df['Categoria'].unique(), default=df['Categoria'].unique())
    
    st.divider()
    st.info("Logado como: **Leomy Ferreira**")
    st.caption("Versão 1.0 - Dashboard Estratégico")

df_filtrado = df[df['Categoria'].isin(categorias)]

# 4. ÁREA PRINCIPAL
st.title("📊 Painel Executivo de Gestão")
st.write("Análise de desempenho de vendas e níveis críticos de estoque.")

# Linha de Métricas (KPIs)
m1, m2, m3, m4 = st.columns(4)
faturamento_total = df_filtrado['Total_Vendas_RS'].sum()
itens_criticos = df_filtrado[df_filtrado['Status'] == '🚨 Repor'].shape[0]

m1.metric("Faturamento Mensal", f"R$ {faturamento_total:,.2f}", "+8.2%")
m2.metric("Itens Críticos", itens_criticos, delta="-2 itens", delta_color="inverse")
m3.metric("Ticket Médio", f"R$ {df_filtrado['Preco_Venda'].mean():,.2f}")
m4.metric("Itens em Estoque", df_filtrado['Estoque'].sum())

st.markdown("<br>", unsafe_allow_html=True)

# 5. GRÁFICOS
c1, c2 = st.columns([0.6, 0.4])

with c1:
    st.subheader("Nível de Estoque por Medicamento")
    fig_est = px.bar(
        df_filtrado, x="Produto", y="Estoque", 
        color="Status", 
        color_discrete_map={'✅ OK': '#00CC96', '🚨 Repor': '#EF553B'},
        template="plotly_white",
        text_auto=True
    )
    st.plotly_chart(fig_est, use_container_width=True)

with c2:
    st.subheader("Distribuição de Faturamento")
    fig_pie = px.pie(
        df_filtrado, values='Total_Vendas_RS', names='Categoria',
        hole=0.5, 
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# 6. TABELA DETALHADA
st.subheader("📋 Detalhamento do Inventário")
st.dataframe(
    df_filtrado.sort_values(by="Status", ascending=False), 
    use_container_width=True,
    hide_index=True
)

st.divider()
st.caption("Desenvolvido para análise ágil de pequenas e médias drogarias.")