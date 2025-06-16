import streamlit as st
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

class Page(ABC):
    @abstractmethod
    def show(self):
        pass

class EstoquePage(Page):
    def __init__(self, text_path: str):
        self.text_path = Path(text_path)
        self.dados = self._load_data()
        if "produtos" not in st.session_state:
            st.session_state["produtos"] = [
                {"id": "PROD001", "categoria": "Bebidas", "nome": "Vinho Tinto", "quantidade": 50},
                {"id": "PROD002", "categoria": "Bebidas", "nome": "Vinho Branco", "quantidade": 40},
                {"id": "PROD003", "categoria": "Bebidas", "nome": "Vinho Rosé", "quantidade": 30},
                {"id": "PROD004", "categoria": "Queijos", "nome": "Queijo Brie", "quantidade": 20},
                {"id": "PROD005", "categoria": "Utensílios", "nome": "Saca-rolhas", "quantidade": 15},
            ]
        if "acao_produto" not in st.session_state:
            st.session_state["acao_produto"] = None
        if "modo" not in st.session_state:
            st.session_state["modo"] = None

    def _load_data(self):
        with open(self.text_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def show(self):
        st.title(f"Bem-vindo, Usuario!")
        st.subheader("Página de Estoque")
        st.markdown("---")

        # Barra de pesquisa
        col_pesquisa = st.columns([0.2, 0.8])
        with col_pesquisa[0]:
            pesquisa_id = st.text_input("", placeholder="Pesquisar por ID...", key="pesquisa_id")

        # Filtro
        col_filtro = st.columns([0.2, 0.8])
        with col_filtro[0]:
            with st.expander("Filtro"):
                categorias = sorted(set(p["categoria"] for p in st.session_state["produtos"]))
                categoria_selecionada = st.radio("Escolha a categoria:", ["Todas"] + categorias)

        st.markdown("---")

        # Filtra os produtos
        produtos_filtrados = [p for p in st.session_state["produtos"]]
        if categoria_selecionada != "Todas":
            produtos_filtrados = [p for p in produtos_filtrados if p["categoria"] == categoria_selecionada]
        if pesquisa_id:
            produtos_filtrados = [p for p in produtos_filtrados if pesquisa_id.lower() in p["id"].lower()]

        for i, produto in enumerate(produtos_filtrados):
            col_info, col_qtd, col_compra, col_venda = st.columns([3, 1, 1, 1])
            with col_info:
                st.write(f"**{produto['nome']}**")
                st.write(f"ID: {produto['id']}")
                st.write(f"Categoria: {produto['categoria']}")
            with col_qtd:
                st.write(f"Quantidade: {produto['quantidade']}")
            with col_compra:
                if st.button("COMPRA", key=f"compra_{produto['id']}"):
                    st.session_state["acao_produto"] = produto["id"]
                    st.session_state["modo"] = "compra"
            with col_venda:
                if st.button("VENDA", key=f"venda_{produto['id']}"):
                    st.session_state["acao_produto"] = produto["id"]
                    st.session_state["modo"] = "venda"
            st.markdown("---")

            if st.session_state["acao_produto"] == produto["id"]:
                with st.container():
                    st.subheader(f"{st.session_state['modo'].upper()} - {produto['nome']}")
                    qtd = st.number_input("Quantidade:", min_value=1, step=1, key=f"qtd_input_{produto['id']}")
                    cols_botoes = st.columns([1, 1])
                    with cols_botoes[0]:
                        if st.button("Confirmar", key=f"confirmar_{produto['id']}"):
                            if st.session_state["modo"] == "compra":
                                produto['quantidade'] += qtd
                                st.success(f"Adicionado {qtd} unidades ao estoque!")
                            elif st.session_state["modo"] == "venda":
                                if produto['quantidade'] - qtd >= 0:
                                    produto['quantidade'] -= qtd
                                    st.success(f"Vendidas {qtd} unidades!")
                                else:
                                    st.error("Não há estoque suficiente para essa venda.")
                            st.session_state["acao_produto"] = None
                            st.session_state["modo"] = None
                            try:
                                st.rerun()
                            except AttributeError:
                                st.experimental_rerun()
                    with cols_botoes[1]:
                        if st.button("Cancelar", key=f"cancelar_{produto['id']}"):
                            st.session_state["acao_produto"] = None
                            st.session_state["modo"] = None
                            try:
                                st.rerun()
                            except AttributeError:
                                st.experimental_rerun()
                    st.markdown("---")  

        