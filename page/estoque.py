import streamlit as st
import json
from pathlib import Path
from abc import ABC, abstractmethod
import mysql.connector
from mysql.connector import Error

# Importa a classe que contém o método de conexão estático
from src.Gerenciadores.gerenciadorLogin import GerenciadorLogin

class Page(ABC):
    @abstractmethod
    def show(self):
        ...

class EstoquePage(Page):
    def __init__(self, text_path: str):
        self.text_path = Path(text_path)
        # O estado da interface (qual pop-up abrir) é gerenciado pelo Streamlit
        st.session_state.setdefault("acao_produto", None)
        st.session_state.setdefault("modo", None)

    # ---------- Conexão e Utilitários de Banco de Dados ------------

    def _carregar_produtos(self, empresa_id: int):
        """
        Carrega apenas os produtos da empresa especificada.
        Abre e fecha a conexão para garantir que não haja conexões ociosas.
        """
        conn = GerenciadorLogin._conectar()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                # Query SQL modificada para filtrar por empresa
                cursor.execute("SELECT * FROM produtos WHERE empresa_id = %s", (empresa_id,))
                return cursor.fetchall()
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        return []

    def _registrar_transacao_e_atualizar_estoque(self, prod_id: int, usuario_id: int, tipo_acao: str, qtd_alterada: int):
        """
        Executa a lógica de compra/venda como uma transação atômica no banco de dados.
        Isso garante que o estoque só é atualizado se o histórico for registrado com sucesso.
        """
        conn = GerenciadorLogin._conectar()
        if not conn:
            return False, "Falha na conexão com o banco de dados."

        try:
            cursor = conn.cursor()
            conn.start_transaction()

            # 1. Busca a quantidade atual do produto, travando a linha para evitar concorrência
            cursor.execute("SELECT quantidade FROM produtos WHERE id = %s FOR UPDATE", (prod_id,))
            resultado = cursor.fetchone()
            if not resultado:
                conn.rollback()
                return False, "Produto não encontrado."
            
            qtd_anterior = resultado[0]

            # 2. Valida a transação
            if tipo_acao == "venda" and qtd_anterior < qtd_alterada:
                conn.rollback()
                return False, "Estoque insuficiente."

            # 3. Calcula a nova quantidade e atualiza a tabela de produtos
            qtd_nova = qtd_anterior + qtd_alterada if tipo_acao == "compra" else qtd_anterior - qtd_alterada
            cursor.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (qtd_nova, prod_id))

            # 4. Insere o registro na tabela de histórico
            sql_log = """
                INSERT INTO historico_transacoes 
                (produto_id, usuario_id, tipo, quantidade_alterada, quantidade_anterior, quantidade_nova) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            dados_log = (prod_id, usuario_id, tipo_acao, qtd_alterada, qtd_anterior, qtd_nova)
            cursor.execute(sql_log, dados_log)
            
            # 5. Se tudo deu certo, comita a transação
            conn.commit()
            return True, "Operação realizada com sucesso!"

        except Error as e:
            # Se qualquer passo falhar, desfaz todas as alterações
            conn.rollback()
            return False, f"Ocorreu um erro: {e}"
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    # ---------- Interface Streamlit ---------
    def show(self):
        st.title("Página de Estoque")
        st.markdown("---")

        # Pré-requisito: o ID do usuário e da empresa devem estar no session_state após o login
        if 'usuario_id' not in st.session_state or 'empresa_id' not in st.session_state:
            st.warning("Por favor, faça o login para acessar o estoque.")
            st.stop()

        empresa_id_logado = st.session_state['empresa_id']
        produtos = self._carregar_produtos(empresa_id_logado)

        if not produtos:
            st.info("Nenhum produto cadastrado para esta empresa.")
            return

        # Interface de filtros e pesquisa (seu código original)
        # ...

        # ---------- Listagem dos produtos ----------
        for produto in produtos:
            col_info, col_qtd, col_compra, col_venda = st.columns([3, 1, 1, 1])
            with col_info:
                st.write(f"**{produto['nome']}**")
                st.write(f"ID: {produto['id']} | Categoria: {produto['categoria']}")
            with col_qtd:
                st.write(f"Quantidade: {produto['quantidade']}")
            
            with col_compra:
                if st.button("COMPRA", key=f"compra_{produto['id']}"):
                    st.session_state.acao_produto = produto["id"]
                    st.session_state.modo = "compra"
            with col_venda:
                if st.button("VENDA", key=f"venda_{produto['id']}"):
                    st.session_state.acao_produto = produto["id"]
                    st.session_state.modo = "venda"
            st.markdown("---")

            # ---------- Formulário compra/venda ----------
            if st.session_state.acao_produto == produto["id"]:
                st.subheader(f"{st.session_state.modo.upper()} - {produto['nome']}")
                qtd = st.number_input("Quantidade:", min_value=1, step=1, key=f"qtd_{produto['id']}")

                col_ok, col_cancel = st.columns(2)
                with col_ok:
                    if st.button("Confirmar", key=f"ok_{produto['id']}"):
                        
                        sucesso, mensagem = self._registrar_transacao_e_atualizar_estoque(
                            prod_id=produto["id"],
                            usuario_id=st.session_state['usuario_id'],
                            tipo_acao=st.session_state.modo,
                            qtd_alterada=qtd
                        )
                        
                        if sucesso:
                            st.success(mensagem)
                        else:
                            st.error(mensagem)

                        st.session_state.acao_produto = None
                        st.session_state.modo = None
                        st.rerun()

                with col_cancel:
                    if st.button("Cancelar", key=f"cancel_{produto['id']}"):
                        st.session_state.acao_produto = None
                        st.session_state.modo = None
                        st.rerun()