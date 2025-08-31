# src/models.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from datetime import datetime

class DataLoaderConfig(BaseModel):
    """Configuração para carregamento de dados."""
    url: str
    chave: str
    coluna_valor: str
    prefixos_remover: Optional[List[str]] = []

class VendaModel(BaseModel):
    """Modelo para dados de venda."""
    cliente: str = Field(..., min_length=1)
    valor_compra: float = Field(..., gt=0)
    data_venda: datetime
    
    @field_validator('cliente')
    @classmethod
    def limpar_cliente(cls, v: str) -> str:
        """Validador para limpar o nome do cliente."""
        return v.lower().strip()

class LocacaoModel(BaseModel):
    """Modelo para dados de locação."""
    apartamento: str = Field(..., min_length=1)
    valor_aluguel: float = Field(..., gt=0)
    data_combinada_pagamento: datetime
    data_pagamento: datetime
    
    @field_validator('apartamento')
    @classmethod
    def limpar_apartamento(cls, v: str) -> str:
        """Validador para limpar o nome do apartamento."""
        return v.replace('(blocoAP)', '').strip()
    
    @property
    def atraso_dias(self) -> int:
        """Calcula atraso em dias."""
        return (self.data_pagamento - self.data_combinada_pagamento).days

class RelatorioVendas(BaseModel):
    """Modelo para relatório de vendas."""
    cliente_vencedor: str
    valor_vencedor: float
    total_clientes: int
    valor_total_evento: float
    valor_medio_por_cliente: float
    duracao_evento_dias: int
    top_5_clientes: Dict[str, float]
    data_inicio: datetime
    data_fim: datetime

class RelatorioAlugueis(BaseModel):
    """Modelo para relatório de aluguéis."""
    apartamento_mais_atrasado: str
    atraso_maximo_medio: float
    apartamento_mais_pontual: str
    atraso_minimo_medio: float
    total_apartamentos: int
    atraso_medio_geral: float
    distribuicao_pontualidade: Dict[str, int]
    ranking_atrasos: Dict[str, float]
