import streamlit as st
import json
from pathlib import Path
from abc import ABC, abstractmethod

import mysql.connector          # ← novo
import hashlib                  #  idem

from src.geral import *
from src.Gerenciadores.gerenciadorLogin import *

class Page(ABC):
    @abstractmethod
    def show(self):
        ...

class EstoquePage(Page):
    def __init__(self, text_path: str):
        self.text_path = Path(text_path)
        self.dados = self._load_data()

        # ------- Conexão com o banco ----------
        self.conn = Pages.conectar()
        self.cursor = self.conn.cursor(dictionary=True)

        # ------- Carrega produtos do BD --------
        if "produtos" not in st.session_state:
            st.session_state["produtos"] = self._carregar_produtos()

        # Estados auxiliares
        st.session_state.setdefault("acao_produto", None)
        st.session_state.setdefault("modo", None)

    # ---------- utilidades de BD ------------
    def _carregar_produtos(self):
        self.cursor.execute("SELECT * FROM produtos")
        return self.cursor.fetchall()

    def _salvar_quantidade(self, prod_id: str, nova_qtd: int):
        self.cursor.execute(
            "UPDATE produtos SET quantidade = %s WHERE id = %s",
            (nova_qtd, prod_id)
        )
        self.conn.commit()

    # ---------- utilidades de arquivo -------
    def _load_data(self):
        with open(self.text_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------- interface Streamlit ---------
    def show(self):
        st.title("Bem-vindo, Usuário!")
        st.subheader("Página de Estoque")
        st.markdown("---")

        # 🔎 Barra de pesquisa
        col_pesq = st.columns([0.2, 0.8])
        with col_pesq[0]:
            pesquisa_id = st.text_input("", placeholder="Pesquisar por ID...", key="pesquisa_id")

        # 🏷️ Filtro
        col_filt = st.columns([0.2, 0.8])
        with col_filt[0]:
            with st.expander("Filtro"):
                categorias = sorted({p["categoria"] for p in st.session_state["produtos"]})
                categoria_selecionada = st.radio("Escolha a categoria:", ["Todas"] + categorias)

        st.markdown("---")

        # Aplica filtros
        produtos = st.session_state["produtos"]
        if categoria_selecionada != "Todas":
            produtos = [p for p in produtos if p["categoria"] == categoria_selecionada]
        if pesquisa_id:
            produtos = [p for p in produtos if pesquisa_id.lower() in p["id"].lower()]

        # ---------- Listagem dos produtos ----------
        for produto in produtos:
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

            # ---------- Formulário compra/venda ----------
            if st.session_state["acao_produto"] == produto["id"]:
                st.subheader(f"{st.session_state['modo'].upper()} - {produto['nome']}")
                qtd = st.number_input("Quantidade:", min_value=1, step=1, key=f"qtd_{produto['id']}")

                col_ok, col_cancel = st.columns(2)
                with col_ok:
                    if st.button("Confirmar", key=f"ok_{produto['id']}"):
                        if st.session_state["modo"] == "compra":
                            nova_qtd = produto["quantidade"] + qtd
                            produto["quantidade"] = nova_qtd
                            st.success(f"Adicionado {qtd} unidades!")
                        else:  # venda
                            if produto["quantidade"] >= qtd:
                                nova_qtd = produto["quantidade"] - qtd
                                produto["quantidade"] = nova_qtd
                                st.success(f"Vendidas {qtd} unidades!")
                            else:
                                st.error("Estoque insuficiente.")
                                return

                        # 💾 persiste no banco
                        self._salvar_quantidade(produto["id"], produto["quantidade"])

                        # Reseta estado e recarrega da fonte oficial
                        st.session_state["acao_produto"] = None
                        st.session_state["modo"] = None
                        st.session_state["produtos"] = self._carregar_produtos()
                        st.experimental_rerun()

                with col_cancel:
                    if st.button("Cancelar", key=f"cancel_{produto['id']}"):
                        st.session_state["acao_produto"] = None
                        st.session_state["modo"] = None
                        st.experimental_rerun()

    # ---------- limpeza ----------
    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except AttributeError:
            pass
