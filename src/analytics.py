import pandas as pd
from typing import Tuple, Dict, List
from .models import RelatorioVendas, RelatorioAlugueis # Importe os modelos de relatório

class AnalisadorVendas:
    """Analisador de dados de vendas com Pydantic"""
    
    def __init__(self, dados_vendas: pd.DataFrame):
        self.dados_vendas = dados_vendas
    
    def calcular_total_por_cliente(self) -> pd.Series:
        """Calcula total de compras por cliente"""
        return (self.dados_vendas
                .groupby('Cliente')['Valor da compra']
                .sum()
                .sort_values(ascending=False))
    
    def identificar_cliente_vencedor(self) -> Tuple[str, float]:
        """Identifica cliente com maior compra"""
        total_compras = self.calcular_total_por_cliente()
        return total_compras.index[0], total_compras.iloc[0]
    
    def gerar_relatorio(self) -> RelatorioVendas:
        """Gera relatório estruturado com Pydantic"""
        total_compras = self.calcular_total_por_cliente()
        cliente_vencedor, valor_vencedor = self.identificar_cliente_vencedor()
        
        return RelatorioVendas(
            cliente_vencedor=cliente_vencedor,
            valor_vencedor=valor_vencedor,
            total_clientes=len(total_compras),
            valor_total_evento=total_compras.sum(),
            valor_medio_por_cliente=total_compras.mean(),
            duracao_evento_dias=(self.dados_vendas['Data de venda'].max() - 
                               self.dados_vendas['Data de venda'].min()).days + 1,
            top_5_clientes=total_compras.head(5).to_dict(),
            data_inicio=self.dados_vendas['Data de venda'].min(),
            data_fim=self.dados_vendas['Data de venda'].max()
        )


class AnalisadorAluguel:
    """Analisador de dados de aluguel com Pydantic"""
    
    def __init__(self, dados_locacao: pd.DataFrame):
        self.dados_locacao = dados_locacao
    
    def calcular_atrasos(self) -> pd.DataFrame:
        """Calcula atrasos nos pagamentos"""
        df_copy = self.dados_locacao.copy()
        df_copy['atraso'] = (df_copy['datas_de_pagamento'] - 
                            df_copy['datas_combinadas_pagamento']).dt.days
        return df_copy
    
    def calcular_media_atraso_por_apartamento(self) -> pd.Series:
        """Calcula média de atraso por apartamento"""
        dados_com_atraso = self.calcular_atrasos()
        return (dados_com_atraso
                .groupby('apartamento')['atraso']
                .mean()
                .sort_values(ascending=False))
    
    def classificar_apartamentos(self) -> Dict[str, List[str]]:
        """Classifica apartamentos por pontualidade"""
        media_atraso = self.calcular_media_atraso_por_apartamento()
        
        return {
            'pontuais': media_atraso[media_atraso <= 0].index.tolist(),
            'atraso_leve': media_atraso[(media_atraso > 0) & (media_atraso <= 5)].index.tolist(),
            'atraso_moderado': media_atraso[(media_atraso > 5) & (media_atraso <= 15)].index.tolist(),
            'atraso_severo': media_atraso[media_atraso > 15].index.tolist()
        }
    
    def gerar_relatorio(self) -> RelatorioAlugueis:
        """Gera relatório estruturado com Pydantic"""
        media_atraso = self.calcular_media_atraso_por_apartamento()
        distribuicao = self.classificar_apartamentos()
        
        return RelatorioAlugueis(
            apartamento_mais_atrasado=media_atraso.index[0],
            atraso_maximo_medio=media_atraso.iloc[0],
            apartamento_mais_pontual=media_atraso.index[-1],
            atraso_minimo_medio=media_atraso.iloc[-1],
            total_apartamentos=len(media_atraso),
            atraso_medio_geral=self.calcular_atrasos()['atraso'].mean(),
            distribuicao_pontualidade={k: len(v) for k, v in distribuicao.items()},
            ranking_atrasos=media_atraso.head(10).to_dict()
        )
