import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional
import pandas as pd
from .models import RelatorioVendas, RelatorioAlugueis # Importe os modelos de relatório
from matplotlib.patches import Patch # Necessário para a legenda personalizada

class VisualizadorVendas:
    """Visualizações para análise de vendas"""
    
    def __init__(self, relatorio: RelatorioVendas, dados: pd.DataFrame):
        self.relatorio = relatorio
        self.dados = dados
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def plot_top_clientes(self, top_n: int = 10, figsize: tuple = (12, 8)) -> plt.Figure:
        """Gráfico dos top clientes"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Gráfico de barras horizontais
        top_clientes = pd.Series(self.relatorio.top_5_clientes)
        top_clientes.plot(kind='barh', ax=ax1, color='skyblue')
        ax1.set_title('Top 5 Clientes por Valor de Compra', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Valor Total (R$)')
        ax1.grid(axis='x', alpha=0.3)
        
        # Gráfico de pizza - distribuição percentual
        top_5_total = sum(self.relatorio.top_5_clientes.values())
        outros_total = self.relatorio.valor_total_evento - top_5_total
        
        labels = list(self.relatorio.top_5_clientes.keys()) + ['Outros Clientes']
        sizes = list(self.relatorio.top_5_clientes.values()) + [outros_total]
        
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Distribuição de Vendas - Top 5 vs Outros', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def plot_vendas_por_dia(self, figsize: tuple = (12, 6)) -> plt.Figure:
        """Gráfico de vendas por dia"""
        fig, ax = plt.subplots(figsize=figsize)
        vendas_diarias = (self.dados.groupby(self.dados['Data de venda'].dt.date)
                         ['Valor da compra'].sum())
        
        vendas_diarias.plot(kind='line', marker='o', linewidth=2, markersize=8, ax=ax)
        ax.set_title('Evolução das Vendas Durante o Evento', fontsize=16, fontweight='bold')
        ax.set_xlabel('Data')
        ax.set_ylabel('Valor Total (R$)')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    
    def plot_estatisticas_resumo(self, figsize: tuple = (15, 10)) -> plt.Figure:
        """Dashboard completo de vendas"""
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Métricas principais
        ax1 = fig.add_subplot(gs[0, :])
        metricas = [
            f'Total Clientes: {self.relatorio.total_clientes}',
            f'Valor Total: R$ {self.relatorio.valor_total_evento:,.2f}',
            f'Ticket Médio: R$ {self.relatorio.valor_medio_por_cliente:.2f}',
            f'Duração: {self.relatorio.duracao_evento_dias} dias'
        ]
        
        ax1.text(0.5, 0.5, ' | '.join(metricas), ha='center', va='center', 
                fontsize=14, fontweight='bold', transform=ax1.transAxes)
        ax1.axis('off')
        ax1.set_title('Resumo Executivo do Evento de Vendas', fontsize=18, fontweight='bold', pad=20)
        
        # Destaque do cliente vencedor
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.bar(['Cliente Vencedor'], [self.relatorio.valor_vencedor], color='gold', width=0.5)
        ax2.set_title('🏆 Cliente Premiado', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Valor (R$)')
        ax2.text(0, self.relatorio.valor_vencedor/2, self.relatorio.cliente_vencedor.title(), 
                ha='center', va='center', fontweight='bold')
        
        # Top 5 clientes
        ax3 = fig.add_subplot(gs[1, 1:])
        top_5 = pd.Series(self.relatorio.top_5_clientes)
        top_5.plot(kind='bar', ax=ax3, color='lightcoral')
        ax3.set_title('Top 5 Clientes', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Valor (R$)')
        ax3.tick_params(axis='x', rotation=45)
        
        # Vendas por dia
        ax4 = fig.add_subplot(gs[2, :])
        vendas_diarias = (self.dados.groupby(self.dados['Data de venda'].dt.date)
                         ['Valor da compra'].sum())
        vendas_diarias.plot(kind='line', ax=ax4, marker='o', color='green')
        ax4.set_title('Vendas por Dia', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Valor (R$)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout() # Adicione isto para evitar sobreposição
        return fig


class VisualizadorAlugueis:
    """Visualizações para análise de aluguéis"""
    
    def __init__(self, relatorio: RelatorioAlugueis, dados: pd.DataFrame):
        self.relatorio = relatorio
        self.dados = dados
        plt.style.use('seaborn-v0_8')
    
    def plot_distribuicao_atrasos(self, figsize: tuple = (12, 8)) -> plt.Figure:
        """Gráfico da distribuição de atrasos"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Gráfico de pizza - categorias de atraso
        labels = ['Pontuais', 'Atraso Leve', 'Atraso Moderado', 'Atraso Severo']
        sizes = [self.relatorio.distribuicao_pontualidade[k] for k in 
                ['pontuais', 'atraso_leve', 'atraso_moderado', 'atraso_severo']]
        colors = ['green', 'yellow', 'orange', 'red']
        
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribuição de Pontualidade dos Moradores', fontsize=14, fontweight='bold')
        
        # Histograma de atrasos
        atrasos = (self.dados['datas_de_pagamento'] - self.dados['datas_combinadas_pagamento']).dt.days
        ax2.hist(atrasos, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.axvline(atrasos.mean(), color='red', linestyle='--', linewidth=2, 
                   label=f'Média: {atrasos.mean():.1f} dias')
        ax2.set_title('Distribuição de Atrasos (Dias)', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Dias de Atraso')
        ax2.set_ylabel('Frequência')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_ranking_apartamentos(self, top_n: int = 15, figsize: tuple = (14, 8)) -> plt.Figure:
        """Gráfico do ranking de apartamentos mais atrasados"""
        ranking = pd.Series(self.relatorio.ranking_atrasos).head(top_n)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Define cores baseadas no nível de atraso
        colors = []
        for atraso in ranking.values:
            if atraso > 15:
                colors.append('red')
            elif atraso > 5:
                colors.append('orange')
            elif atraso > 0:
                colors.append('yellow')
            else:
                colors.append('green')
        
        bars = ax.bar(range(len(ranking)), ranking.values, color=colors, alpha=0.7)
        
        # Adiciona valores nas barras
        for i, (apt, atraso) in enumerate(ranking.items()):
            ax.text(i, atraso + 0.5, f'{atraso:.1f}d', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title(f'Top {top_n} Apartamentos com Maior Atraso Médio', fontsize=16, fontweight='bold')
        ax.set_xlabel('Apartamentos')
        ax.set_ylabel('Atraso Médio (Dias)')
        ax.set_xticks(range(len(ranking)))
        ax.set_xticklabels(ranking.index, rotation=45, ha='right')
        
        # Legenda de cores
        legend_elements = [
            Patch(facecolor='red', label='Severo (>15 dias)'),
            Patch(facecolor='orange', label='Moderado (5-15 dias)'),
            Patch(facecolor='yellow', label='Leve (0-5 dias)'),
            Patch(facecolor='green', label='Pontual (≤0 dias)')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        return fig
    
    def plot_dashboard_alugueis(self, figsize: tuple = (16, 12)) -> plt.Figure:
        """Dashboard completo de aluguéis"""
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(4, 3, hspace=0.4, wspace=0.3)
        
        # Título principal
        fig.suptitle('Dashboard de Análise de Aluguéis - Gestão de Condomínio', 
                    fontsize=20, fontweight='bold', y=0.98)
        
        # Métricas principais
        ax1 = fig.add_subplot(gs[0, :])
        metricas_text = f"""
        Total de Apartamentos: {self.relatorio.total_apartamentos} | 
        Atraso Médio Geral: {self.relatorio.atraso_medio_geral:.1f} dias | 
        Apartamento Mais Atrasado: {self.relatorio.apartamento_mais_atrasado} ({self.relatorio.atraso_maximo_medio:.1f}d) | 
        Apartamento Mais Pontual: {self.relatorio.apartamento_mais_pontual} ({self.relatorio.atraso_minimo_medio:.1f}d)
        """
        ax1.text(0.5, 0.5, metricas_text, ha='center', va='center', fontsize=12, 
                fontweight='bold', transform=ax1.transAxes)
        ax1.axis('off')
        
        # Distribuição de pontualidade (pizza)
        ax2 = fig.add_subplot(gs[1, 0])
        labels = ['Pontuais', 'Leve', 'Moderado', 'Severo']
        sizes = [self.relatorio.distribuicao_pontualidade[k] for k in 
                ['pontuais', 'atraso_leve', 'atraso_moderado', 'atraso_severo']]
        colors = ['green', 'yellow', 'orange', 'red']
        ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.0f', startangle=90)
        ax2.set_title('Distribuição de Pontualidade', fontsize=12, fontweight='bold')
        
        # Top 10 apartamentos mais atrasados
        ax3 = fig.add_subplot(gs[1, 1:])
        top_10 = pd.Series(self.relatorio.ranking_atrasos).head(10)
        colors_bar = ['red' if x > 15 else 'orange' if x > 5 else 'yellow' if x > 0 else 'green' 
                     for x in top_10.values]
        top_10.plot(kind='bar', ax=ax3, color=colors_bar)
        ax3.set_title('Top 10 Apartamentos Mais Atrasados', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Atraso Médio (Dias)')
        ax3.tick_params(axis='x', rotation=45)
        
        # Histograma de todos os atrasos
        ax4 = fig.add_subplot(gs[2, :])
        atrasos = (self.dados['datas_de_pagamento'] - self.dados['datas_combinadas_pagamento']).dt.days
        ax4.hist(atrasos, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        ax4.axvline(atrasos.mean(), color='red', linestyle='--', linewidth=2, 
                   label=f'Média: {atrasos.mean():.1f} dias')
        ax4.axvline(0, color='green', linestyle='-', linewidth=2, alpha=0.7, label='Pontualidade Ideal')
        ax4.set_title('Distribuição Completa de Atrasos', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Dias de Atraso')
        ax4.set_ylabel('Frequência de Pagamentos')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Análise temporal (se houver dados suficientes)
        ax5 = fig.add_subplot(gs[3, :])
        if 'datas_de_pagamento' in self.dados.columns:
            atrasos_mensais = (self.dados.groupby(self.dados['datas_de_pagamento'].dt.to_period('M'))
                              .apply(lambda x: ((x['datas_de_pagamento'] - x['datas_combinadas_pagamento'])
                                               .dt.days.mean())))
            if len(atrasos_mensais) > 1:
                atrasos_mensais.plot(kind='line', ax=ax5, marker='o', linewidth=2, markersize=8)
                ax5.set_title('Evolução do Atraso Médio por Mês', fontsize=12, fontweight='bold')
                ax5.set_ylabel('Atraso Médio (Dias)')
                ax5.grid(True, alpha=0.3)
            else:
                ax5.text(0.5, 0.5, 'Dados insuficientes para análise temporal', 
                        ha='center', va='center', transform=ax5.transAxes)
                ax5.axis('off')
        
        plt.tight_layout()
        return fig
