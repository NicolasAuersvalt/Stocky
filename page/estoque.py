import streamlit as st
import json
from pathlib import Path
from abc import ABC, abstractmethod
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Importações para a funcionalidade de exportação
import pandas as pd
from fpdf import FPDF
import io

# Importa a classe que contém o método de conexão estático
from src.Gerenciadores.gerenciadorLogin import GerenciadorLogin

class Page(ABC):
    @abstractmethod
    def show(self):
        ...

class EstoquePage(Page):
    def __init__(self, text_path: str):
        self.text_path = Path(text_path)
        st.session_state.setdefault("acao_produto", None)
        st.session_state.setdefault("modo", None)

    def _carregar_produtos(self, empresa_id: int):
        """Carrega apenas os produtos da empresa especificada."""
        conn = GerenciadorLogin._conectar()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM produtos WHERE empresa_id = %s", (empresa_id,))
                return cursor.fetchall()
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        return []

    def _registrar_transacao_e_atualizar_estoque(self, prod_id: int, usuario_id: int, tipo_acao: str, qtd_alterada: int, preco_unitario: float):
        """Executa a lógica de compra/venda e registra no histórico."""
        conn = GerenciadorLogin._conectar()
        if not conn:
            return False, "Falha na conexão com o banco de dados."
        try:
            cursor = conn.cursor()
            conn.start_transaction()
            cursor.execute("SELECT quantidade FROM produtos WHERE id = %s FOR UPDATE", (prod_id,))
            resultado = cursor.fetchone()
            if not resultado:
                conn.rollback()
                return False, "Produto não encontrado."
            
            qtd_anterior = resultado[0]

            if tipo_acao == "venda" and qtd_anterior < qtd_alterada:
                conn.rollback()
                return False, "Estoque insuficiente."

            qtd_nova = qtd_anterior + qtd_alterada if tipo_acao == "compra" else qtd_anterior - qtd_alterada
            cursor.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (qtd_nova, prod_id))
            
            sql_log = """
                INSERT INTO historico_transacoes 
                (produto_id, usuario_id, tipo, quantidade_alterada, preco_transacao, quantidade_anterior, quantidade_nova) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            dados_log = (prod_id, usuario_id, tipo_acao, qtd_alterada, preco_unitario, qtd_anterior, qtd_nova)
            cursor.execute(sql_log, dados_log)
            
            conn.commit()
            return True, "Operação realizada com sucesso!"
        except Error as e:
            conn.rollback()
            return False, f"Ocorreu um erro: {e}"
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def _buscar_historico_completo(self, empresa_id: int):
        """Busca um histórico detalhado das transações para uma empresa."""
        conn = GerenciadorLogin._conectar()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                sql_query = """
                    SELECT 
                        h.data_transacao,
                        p.nome AS produto,
                        u.nome AS usuario,
                        h.tipo,
                        h.quantidade_alterada,
                        h.preco_transacao,
                        h.quantidade_anterior,
                        h.quantidade_nova
                    FROM historico_transacoes h
                    JOIN produtos p ON h.produto_id = p.id
                    JOIN usuarios u ON h.usuario_id = u.id
                    WHERE p.empresa_id = %s
                    ORDER BY h.data_transacao DESC
                """
                cursor.execute(sql_query, (empresa_id,))
                return cursor.fetchall()
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        return []

    def _gerar_pdf(self, df: pd.DataFrame):
        """Gera um arquivo PDF a partir de um DataFrame do Pandas."""
        pdf = FPDF(orientation='L')  # Orientação paisagem para mais colunas
        pdf.add_page()
        pdf.set_font("Arial", size=7)
        col_width = pdf.w / (len(df.columns) + 1)
        for col in df.columns:
            pdf.cell(col_width, 10, col.replace('_', ' ').title(), 1, 0, 'C')
        pdf.ln()
        for index, row in df.iterrows():
            for item in row:
                pdf.cell(col_width, 10, str(item), 1, 0)
            pdf.ln()
        return bytes(pdf.output(dest='S'))
    def show(self):
        """Renderiza a página completa de estoque."""
        st.title("Página de Estoque")
        
        if 'usuario_id' not in st.session_state or 'empresa_id' not in st.session_state:
            st.warning("Por favor, faça o login para acessar o estoque.")
            st.stop()

        empresa_id_logado = st.session_state['empresa_id']

        # Seção de Exportação
        st.markdown("---")
        st.subheader("Histórico de Movimentações")
        
        historico_data = self._buscar_historico_completo(empresa_id_logado)
        
        if historico_data:
            df_historico = pd.DataFrame(historico_data)
            st.dataframe(df_historico)
            
            st.markdown("##### Exportar Relatório")
            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                   label="Exportar para .CSV",
                   data=df_historico.to_csv(index=False, sep=';').encode('utf-8'),
                   file_name=f"historico_estoque_{datetime.now().strftime('%Y%m%d')}.csv",
                   mime='text/csv'
                )
            
            with col2:
                pdf_bytes = self._gerar_pdf(df_historico)
                st.download_button(
                    label="Exportar para .PDF",
                    data=pdf_bytes,
                    file_name=f"historico_estoque_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime='application/pdf'
                )
        else:
            st.info("Nenhuma movimentação de estoque registrada para esta empresa.")

        # Seção de Gerenciamento de Produtos
        st.markdown("---")
        st.subheader("Gerenciar Produtos")
        
        produtos = self._carregar_produtos(empresa_id_logado)
        if not produtos:
            st.info("Nenhum produto cadastrado para esta empresa.")
            return

        for produto in produtos:
            col_info, col_qtd, col_compra, col_venda = st.columns([3, 1, 1, 1])
            with col_info:
                st.write(f"**{produto['nome']}**")
                st.write(f"ID: {produto['id']} | Preço: R$ {produto['preco']:.2f}")
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
                            qtd_alterada=qtd,
                            preco_unitario=produto['preco']
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