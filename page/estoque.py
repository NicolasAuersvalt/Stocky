# page/estoque.py

import streamlit as st
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

# Classe base (se quiser reaproveitar com outras páginas)
class Page(ABC):
    @abstractmethod
    def show(self):
        pass

# Classe da página de Estoque
class EstoquePage(Page):
    def __init__(self, text_path: str):
        self.text_path = Path(text_path)
        self.dados = self._load_data()

    def _load_data(self):
        """Carrega os dados do JSON."""
        with open(self.text_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def show(self):
        """Renderiza a página de Estoque no Streamlit."""
        #st.title("Bem-vindo ao Estoque")

        mensagem = self.dados.get("mensagem_inicial", "Mensagem padrão de estoque.")
        st.write(mensagem)
        st.markdown("---")
