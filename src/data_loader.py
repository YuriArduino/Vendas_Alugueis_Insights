import pandas as pd
import numpy as np
from typing import List
import re
from .models import DataLoaderConfig # Importe o modelo DataLoaderConfig

class DataLoader:
    """Carregador de dados otimizado com validação Pydantic"""
    
    def __init__(self):
        self.cache = {}
    
    def carregar_dados(self, config: DataLoaderConfig) -> pd.DataFrame:
        """Carrega dados usando configuração validada"""
        try:
            # Verifica cache
            if config.url in self.cache:
                return self.cache[config.url].copy()
            
            # Carrega dados do JSON
            dados_json = pd.read_json(config.url)
            
            if config.chave not in dados_json:
                raise ValueError(f"Chave '{config.chave}' não encontrada no JSON")
            
            # Normaliza e processa dados
            dados = pd.json_normalize(dados_json[config.chave])
            dados = self._explodir_colunas_lista(dados)
            dados = self._limpar_valores_monetarios(dados, config.coluna_valor, config.prefixos_remover)
            
            # Cache dos dados
            self.cache[config.url] = dados.copy()
            
            return dados
            
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar dados: {str(e)}")
    
    def _explodir_colunas_lista(self, df: pd.DataFrame) -> pd.DataFrame:
        """Explode colunas que contêm listas"""
        colunas_para_explodir = df.columns[1:].tolist()
        if colunas_para_explodir:
            return df.explode(colunas_para_explodir).reset_index(drop=True)
        return df
    
    def _limpar_valores_monetarios(self, df: pd.DataFrame, coluna: str, prefixos: List[str]) -> pd.DataFrame:
        """Limpa e converte valores monetários"""
        if coluna not in df.columns:
            raise KeyError(f"Coluna '{coluna}' não encontrada")
        
        # Remove prefixos
        for prefixo in prefixos:
            df[coluna] = df[coluna].str.replace(prefixo, '', regex=False)
        
        # Padroniza formato
        df[coluna] = (df[coluna]
                     .str.replace(',', '.', regex=False)
                     .str.strip())
        
        # Converte para float
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
        
        return df
    
    @staticmethod
    def processar_datas(df: pd.DataFrame, colunas_data: List[str]) -> pd.DataFrame:
        """Converte colunas para datetime"""
        df_copy = df.copy()
        for coluna in colunas_data:
            if coluna in df_copy.columns:
                df_copy[coluna] = pd.to_datetime(df_copy[coluna], errors='coerce')
        return df_copy
