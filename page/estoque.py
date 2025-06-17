import streamlit as st
import json
from pathlib import Path
from abc import ABC, abstractmethod
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import io

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

    # --- Funções de Banco de Dados ---

    def _carregar_produtos(self, empresa_id: int):
        conn = GerenciadorLogin._conectar()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM produtos WHERE empresa_id = %s", (empresa_id,))
                return cursor.fetchall()
            finally:
                if conn.is_connected(): cursor.close(); conn.close()
        return []

    # ALTERADO: A função agora recebe 'valor_unitario' da transação
    def _registrar_transacao_e_atualizar_estoque(self, prod_id: int, usuario_id: int, tipo_acao: str, qtd_alterada: int, valor_unitario: float):
        conn = GerenciadorLogin._conectar()
        if not conn: return False, "Falha na conexão."

        # Calcula o valor total da transação
        valor_total_transacao = qtd_alterada * valor_unitario
        
        try:
            cursor = conn.cursor()
            conn.start_transaction()
            cursor.execute("SELECT quantidade FROM produtos WHERE id = %s FOR UPDATE", (prod_id,))
            resultado = cursor.fetchone()
            if not resultado: conn.rollback(); return False, "Produto não encontrado."
            
            qtd_anterior = resultado[0]

            if tipo_acao == "venda" and qtd_anterior < qtd_alterada: conn.rollback(); return False, "Estoque insuficiente."
            
            qtd_nova = qtd_anterior + qtd_alterada if tipo_acao == "compra" else qtd_anterior - qtd_alterada
            cursor.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (qtd_nova, prod_id))
            
            # ALTERADO: A query de log agora inclui 'valor_unitario' e 'valor_total'
            sql_log = """
                INSERT INTO historico_transacoes 
                (produto_id, usuario_id, tipo, quantidade_alterada, valor_unitario, valor_total, quantidade_anterior, quantidade_nova) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            dados_log = (prod_id, usuario_id, tipo_acao, qtd_alterada, valor_unitario, valor_total_transacao, qtd_anterior, qtd_nova)
            cursor.execute(sql_log, dados_log)
            
            conn.commit()
            return True, "Operação realizada com sucesso!"
        except Error as e:
            conn.rollback(); return False, f"Ocorreu um erro: {e}"
        finally:
            if conn.is_connected(): cursor.close(); conn.close()

    def _buscar_historico_completo(self, empresa_id: int):
        conn = GerenciadorLogin._conectar()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                # ALTERADO: A query agora busca os novos campos do histórico
                sql_query = """
                    SELECT 
                        h.data_transacao, p.nome AS produto, u.nome AS usuario, h.tipo,
                        h.quantidade_alterada, h.valor_unitario, h.valor_total,
                        h.quantidade_anterior, h.quantidade_nova
                    FROM historico_transacoes h
                    JOIN produtos p ON h.produto_id = p.id
                    JOIN usuarios u ON h.usuario_id = u.id
                    WHERE p.empresa_id = %s ORDER BY h.data_transacao DESC
                """
                cursor.execute(sql_query, (empresa_id,)); return cursor.fetchall()
            finally:
                if conn.is_connected(): cursor.close(); conn.close()
        return []

    def _gerar_pdf(self, df: pd.DataFrame):
        pdf = FPDF(orientation='L'); pdf.add_page(); pdf.set_font("Arial", size=7)
        col_width = pdf.w / (len(df.columns) if df.columns.any() else 1)
        for col in df.columns:
            header = col.replace('_', ' ').title(); pdf.cell(col_width, 10, header, 1, 0, 'C')
        pdf.ln()
        for index, row in df.iterrows():
            for item in row: pdf.cell(col_width, 10, str(item), 1, 0)
            pdf.ln()
        return bytes(pdf.output(dest='S'))

    def show(self):
        st.title("Página de Estoque")
        if 'usuario_id' not in st.session_state or 'empresa_id' not in st.session_state:
            st.warning("Por favor, faça o login para acessar o estoque."); st.stop()

        empresa_id_logado = st.session_state['empresa_id']

        st.markdown("---"); st.subheader("Gerenciar Produtos")
        produtos = self._carregar_produtos(empresa_id_logado)
        if not produtos: st.info("Nenhum produto cadastrado para esta empresa.")
        
        for produto in produtos:
            # ALTERADO: Exibe o valor total em estoque (qtd * preço padrão)
            valor_total_estoque = produto['quantidade'] * produto['preco']
            
            col_info, col_qtd, col_valor_total = st.columns([3, 1, 1])
            with col_info: 
                st.write(f"**{produto['nome']}**")
                st.write(f"ID: {produto['id']} | Preço Padrão: R$ {produto['preco']:.2f}")
            with col_qtd: st.write(f"**Qtd:** {produto['quantidade']}")
            with col_valor_total: st.write(f"**Valor Total:** R$ {valor_total_estoque:.2f}")

            col_compra, col_venda, _ = st.columns([1, 1, 4])
            with col_compra:
                if st.button("COMPRA", key=f"compra_{produto['id']}"): st.session_state.acao_produto = produto["id"]; st.session_state.modo = "compra"
            with col_venda:
                if st.button("VENDA", key=f"venda_{produto['id']}"): st.session_state.acao_produto = produto["id"]; st.session_state.modo = "venda"
            st.markdown("---")

            if st.session_state.acao_produto == produto["id"]:
                with st.form(key=f"form_{produto['id']}"):
                    st.subheader(f"{st.session_state.modo.upper()} - {produto['nome']}")
                    
                    # ALTERADO: Adicionado campo para valor unitário da transação
                    col_form1, col_form2 = st.columns(2)
                    qtd = col_form1.number_input("Quantidade da Transação", min_value=1, step=1, key=f"qtd_{produto['id']}")
                    valor_unit = col_form2.number_input("Valor Unitário (R$)", min_value=0.01, value=float(produto['preco']), format="%.2f", key=f"val_{produto['id']}")

                    submitted = st.form_submit_button("Confirmar")
                    if submitted:
                        # ALTERADO: Passa o 'valor_unit' para a função de registro
                        sucesso, mensagem = self._registrar_transacao_e_atualizar_estoque(
                            prod_id=produto["id"], usuario_id=st.session_state['usuario_id'],
                            tipo_acao=st.session_state.modo, qtd_alterada=qtd,
                            valor_unitario=valor_unit
                        )
                        if sucesso: st.success(mensagem)
                        #else: st.error(mensagem)
                        st.session_state.acao_produto = None; st.session_state.modo = None; st.rerun()

        # Seção de Histórico
        st.markdown("---"); st.subheader("Histórico de Movimentações")
        historico_data = self._buscar_historico_completo(empresa_id_logado)
        
        if historico_data:
            df_historico = pd.DataFrame(historico_data)
            st.dataframe(df_historico)
            st.markdown("##### Exportar Relatório")
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                st.download_button("Exportar para .CSV", df_historico.to_csv(index=False, sep=';').encode('utf-8'), f"historico_{datetime.now().strftime('%Y%m%d')}.csv", 'text/csv')
            with col_exp2:
                pdf_bytes = self._gerar_pdf(df_historico)
                st.download_button("Exportar para .PDF", pdf_bytes, f"historico_{datetime.now().strftime('%Y%m%d')}.pdf", 'application/pdf')
        else:
            st.info("Nenhuma movimentação de estoque registrada.")