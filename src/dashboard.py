# src/dashboard.py

import streamlit as st
import pandas as pd

# Imports relativos para acessar os outros módulos dentro do pacote 'src'
from .analytics import AnalisadorVendas, AnalisadorAluguel
from .visualizations import VisualizadorVendas, VisualizadorAlugueis

def display_vendas_dashboard(analisador_vendas: AnalisadorVendas, dados_vendas: pd.DataFrame):
    """Renderiza a seção de vendas do dashboard."""
    st.header("📊 Análise de Vendas")
    
    # Gera o relatório dentro da função de display
    relatorio_vendas = analisador_vendas.gerar_relatorio()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Clientes", relatorio_vendas.total_clientes)
    col2.metric("Valor Total do Evento", f"R$ {relatorio_vendas.valor_total_evento:,.2f}")
    col3.metric("Ticket Médio", f"R$ {relatorio_vendas.valor_medio_por_cliente:.2f}")
    # A correção está aqui:
    col4.metric("Duração do Evento", f"{relatorio_vendas.duracao_evento_dias} dias")
    
    st.markdown(f"#### 🏆 Cliente Vencedor: *{relatorio_vendas.cliente_vencedor.title()}* com R$ {relatorio_vendas.valor_vencedor:,.2f}")
    st.divider()
    
    viz_vendas = VisualizadorVendas(relatorio_vendas, dados_vendas)
    
    c1, c2 = st.columns(2)
    with c1:
        st.pyplot(viz_vendas.plot_top_clientes(figsize=(8, 6)))
    with c2:
        st.pyplot(viz_vendas.plot_vendas_por_dia(figsize=(8, 6)))
    
    with st.expander("Ver Relatório Detalhado de Vendas (JSON)"):
        st.json(relatorio_vendas.model_dump_json(indent=4))

def display_alugueis_dashboard(analisador_aluguel: AnalisadorAluguel, dados_locacao: pd.DataFrame):
    """Renderiza a seção de aluguéis do dashboard."""
    st.header("🏠 Análise de Aluguéis")

    relatorio_alugueis = analisador_aluguel.gerar_relatorio()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Apartamentos", relatorio_alugueis.total_apartamentos)
    col2.metric("Atraso Médio Geral", f"{relatorio_alugueis.atraso_medio_geral:.1f} dias")
    col3.metric("Apto Mais Atrasado", f"{relatorio_alugueis.apartamento_mais_atrasado} ({relatorio_alugueis.atraso_maximo_medio:.1f}d)")
    st.divider()

    viz_alugueis = VisualizadorAlugueis(relatorio_alugueis, dados_locacao)
    
    c1, c2 = st.columns([0.6, 0.4]) 
    with c1:
         st.pyplot(viz_alugueis.plot_ranking_apartamentos())
    with c2:
        st.pyplot(viz_alugueis.plot_distribuicao_atrasos(figsize=(8, 7)))

    with st.expander("Ver Relatório Detalhado de Aluguéis (JSON)"):
        st.json(relatorio_alugueis.model_dump_json(indent=4))
