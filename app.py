# app.py

import streamlit as st

# Imports do pacote 'src'
from src.models import DataLoaderConfig
from src.data_loader import DataLoader
from src.analytics import AnalisadorVendas, AnalisadorAluguel
from src.dashboard import display_vendas_dashboard, display_alugueis_dashboard

# Configuração da página
st.set_page_config(layout="wide", page_title="Vendas & Aluguéis Insights")

@st.cache_data
def load_and_process_data():
    """Carrega e processa todos os dados. A função permanece aqui
    pois é uma tarefa de 'backend' do app."""
    configs = {
        'vendas': DataLoaderConfig(
            url="https://raw.githubusercontent.com/YuriArduino/Estudos_Pandas/refs/heads/data-tests/dados_vendas_clientes.json",
            chave='dados_vendas',
            coluna_valor='Valor da compra',
            prefixos_remover=['R$ ']
        ),
        'locacao': DataLoaderConfig(
            url="https://raw.githubusercontent.com/YuriArduino/Estudos_Pandas/refs/heads/data-tests/dados_locacao_imoveis.json",
            chave='dados_locacao',
            coluna_valor='valor_aluguel',
            prefixos_remover=['$', ' reais']
        )
    }
    loader = DataLoader()
    dados_vendas = loader.carregar_dados(configs['vendas'])
    dados_vendas['Cliente'] = dados_vendas['Cliente'].str.lower().str.strip()
    dados_vendas = loader.processar_datas(dados_vendas, ['Data de venda'])
    
    dados_locacao = loader.carregar_dados(configs['locacao'])
    dados_locacao['apartamento'] = dados_locacao['apartamento'].str.replace('(blocoAP)', '', regex=False).str.strip()
    dados_locacao = loader.processar_datas(dados_locacao, 
                                         ['datas_combinadas_pagamento', 'datas_de_pagamento'])
    return dados_vendas, dados_locacao

def main():
    """Função principal que orquestra o app Streamlit."""
    st.title("📈 Vendas & Aluguéis Insights")
    st.markdown("Dashboard interativo para análise de dados de vendas e aluguéis.")
    st.divider()

    try:
        # 1. CARREGAR DADOS
        dados_vendas, dados_locacao = load_and_process_data()
        
        # 2. PREPARAR ANÁLISES
        analisador_vendas = AnalisadorVendas(dados_vendas)
        analisador_aluguel = AnalisadorAluguel(dados_locacao)
        
        # 3. RENDERIZAR DASHBOARDS (chamando o módulo de UI)
        display_vendas_dashboard(analisador_vendas, dados_vendas)
        st.divider()
        display_alugueis_dashboard(analisador_aluguel, dados_locacao)

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar ou processar os dados: {e}")
        st.warning("Por favor, verifique sua conexão com a internet ou a URL dos dados.")

if __name__ == "__main__":
    main()
