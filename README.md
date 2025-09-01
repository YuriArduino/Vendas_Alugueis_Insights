# 📈 Vendas & Aluguéis Insights

**[Clique aqui para ver a demonstração ao vivo no Streamlit Cloud](https://vendasalugueisinsights-v3.streamlit.app/#vendas-and-alugueis-insights)**

![Dashboard Screenshot](https://github.com/YuriArduino/Vendas_Alugueis_Insights/blob/main/Captura%20de%20tela%20de%202025-08-31%2021-26-00.png)

## 📄 Visão Geral

Este projeto é um dashboard interativo para análise de dados de vendas e pagamentos de aluguéis. Desenvolvido como projeto final para o curso de Pandas da Alura, ele consolida conhecimentos em limpeza, manipulação, validação e visualização de dados. O objetivo principal foi construir uma aplicação modular, robusta e pronta para produção, culminando na implantação na nuvem via Streamlit Community Cloud.

## ✨ Principais Funcionalidades

-   **Dashboard de Vendas:**
    -   Métricas chave: Valor total, ticket médio e total de clientes.
    -   Identificação e destaque do cliente com maior volume de compras.
    -   Visualização do ranking dos top 5 clientes.
    -   Análise da evolução das vendas ao longo do tempo.
-   **Dashboard de Aluguéis:**
    -   Análise de pontualidade: Atraso médio geral e total de apartamentos monitorados.
    -   Identificação dos apartamentos mais pontuais e dos maiores ofensores.
    -   Ranking visual dos apartamentos com maior média de atraso.
    -   Distribuição percentual da pontualidade dos inquilinos (Pontuais, Atraso Leve, Moderado e Severo).
-   **Validação de Dados com Pydantic:** Garante que os dados processados e os relatórios gerados sejam consistentes e sigam um esquema predefinido.
-   **Estrutura Modular:** O código é organizado em módulos com responsabilidades claras (carregamento de dados, análise, visualização e interface), facilitando a manutenção e escalabilidade.

## 🛠️ Tecnologias Utilizadas

-   **Linguagem:** Python 3
-   **Análise e Manipulação de Dados:** Pandas, NumPy
-   **Validação de Dados:** Pydantic v2
-   **Visualização de Dados:** Matplotlib, Seaborn
-   **Framework da Aplicação Web:** Streamlit
-   **Versionamento de Código:** Git & GitHub
-   **Plataforma de Deploy:** Streamlit Community Cloud

## 📂 Estrutura do Projeto

O projeto segue uma estrutura organizada para separar as responsabilidades do código:


Vendas_Alugueis_Insights/
├── app.py # Script principal e orquestrador do Streamlit
├── requirements.txt # Dependências do projeto
├── .gitignore # Arquivos e pastas ignorados pelo Git
└── src/ # Pacote com todo o código-fonte da aplicação
├── init.py
├── analytics.py # Módulo de análise e cálculos
├── data_loader.py # Módulo para carregar e limpar os dados
├── dashboard.py # Módulo para construir a interface no Streamlit
├── models.py # Módulo com os modelos de dados Pydantic
└── visualizations.py # Módulo para gerar os gráficos



## Como Executar o Projeto Localmente

Para executar este projeto em sua máquina local, siga os passos abaixo.

### Pré-requisitos
-   [Git](https://git-scm.com/)
-   [Python 3.9+](https://www.python.org/)

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/SEU-USUARIO/Vendas_Alugueis_Insights.git
    cd Vendas_Alugueis_Insights
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Linux/macOS
    python3 -m venv venv
    source venv/bin/activate
    ```
    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run app.py
    ```
    A aplicação será aberta automaticamente no seu navegador padrão.

## 🌱 Jornada e Aprendizados

Este projeto marca meu primeiro deploy completo de uma aplicação de dados, desde o ambiente local até a nuvem. A jornada foi repleta de aprendizados valiosos:

-   **Refatoração de Código:** A transição de um script monolítico (comum em notebooks como o Colab) para uma arquitetura modular foi o maior desafio. Dividir o código em `data_loader`, `analytics`, `visualizations` e `dashboard` tornou o projeto imensamente mais legível e fácil de manter.
-   **Pydantic v2:** Atualizei os modelos de dados da v1 para a v2, aprendendo a nova sintaxe de `field_validator` e as melhores práticas da versão mais recente da biblioteca.
-   **Versionamento com Git/GitHub:** Utilizei Git para controlar as versões do projeto de forma incremental e o GitHub como repositório central, uma prática essencial no desenvolvimento de software.
-   **Implantação (Deploy):** O processo de deploy no Streamlit Community Cloud me ensinou sobre a importância de arquivos como `requirements.txt` e como a plataforma automatiza a criação do ambiente e a execução da aplicação.

Este projeto foi um passo fundamental no meu desenvolvimento como profissional de dados, unindo habilidades de análise e engenharia de software para entregar um produto final funcional e acessível.
