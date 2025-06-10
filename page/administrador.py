# page/administrador.py

import streamlit as st
import mysql.connector

class AdmPage:
    def __init__(self):
        # ------- Conexão com o banco ----------
        # MODIFICADO: A classe agora usa seu próprio método para conectar.
        self.conn = self._conectar()
        if self.conn:
            self.cursor = self.conn.cursor(dictionary=True)
        else:
            st.error("Falha na conexão com o banco de dados.")
            st.stop()

        # Estados da aplicação
        st.session_state.setdefault("empresa_selecionada", None)
        st.session_state.setdefault("acao", None)
        st.session_state.setdefault("produto_selecionado_id", None)

    # NOVO: Método de conexão próprio para esta classe.
    # É uma boa prática que cada módulo que acessa o DB gerencie sua própria conexão.
    @staticmethod
    def _conectar():
        try:
            return mysql.connector.connect(
                host=st.secrets["mysql"]["host"],
                user=st.secrets["mysql"]["user"],
                password=st.secrets["mysql"]["password"],
                database=st.secrets["mysql"]["database"]
            )
        except mysql.connector.Error as err:
            st.error(f"Erro ao conectar ao banco de dados: {err}")
            return None

    # ---------- MÉTODOS DE BANCO DE DADOS (CRUD) ------------
    def _carregar_empresas(self):
        # A tabela de empresas agora é consultada pelo seu id na tabela 'empresas'
        self.cursor.execute("SELECT u.id as usuario_id, e.id as empresa_id, e.nome_fantasia FROM empresas e JOIN usuarios u ON e.usuario_id = u.id ORDER BY e.nome_fantasia")
        return self.cursor.fetchall()

    def _carregar_produtos_por_empresa(self, empresa_id):
        self.cursor.execute("SELECT * FROM produtos WHERE empresa_id = %s", (empresa_id,))
        return self.cursor.fetchall()

    def _adicionar_produto(self, nome, categoria, quantidade, preco, empresa_id):
        query = "INSERT INTO produtos (nome, categoria, quantidade, preco, empresa_id) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (nome, categoria, quantidade, preco, empresa_id))
        self.conn.commit()

    def _atualizar_produto(self, produto_id, nome, categoria, quantidade, preco):
        query = "UPDATE produtos SET nome = %s, categoria = %s, quantidade = %s, preco = %s WHERE id = %s"
        self.cursor.execute(query, (nome, categoria, quantidade, preco, produto_id))
        self.conn.commit()

    def _deletar_produto(self, produto_id):
        self.cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
        self.conn.commit()

    # ---------- INTERFACE STREAMLIT ---------
    def _mostrar_formulario_produto(self, produto=None):
        is_alteracao = produto is not None
        titulo = "Alterar Produto" if is_alteracao else "Cadastrar Novo Produto"
        with st.form(key="form_produto"):
            st.subheader(titulo)
            nome = st.text_input("Nome", value=produto["nome"] if is_alteracao else "")
            categoria = st.text_input("Categoria", value=produto["categoria"] if is_alteracao else "")
            col1, col2 = st.columns(2)
            quantidade = col1.number_input("Quantidade", min_value=0, step=1, value=produto["quantidade"] if is_alteracao else 0)
            preco = col2.number_input("Preço (R$)", min_value=0.0, format="%.2f", value=float(produto["preco"]) if is_alteracao else 0.0)
            
            if st.form_submit_button("Salvar"):
                if not nome or not categoria:
                    st.warning("Nome e Categoria são obrigatórios.")
                else:
                    try:
                        if is_alteracao:
                            self._atualizar_produto(produto["id"], nome, categoria, quantidade, preco)
                            st.success("Produto atualizado!")
                        else:
                            # MODIFICADO: Usa o 'empresa_id' que agora é o ID da tabela empresas
                            self._adicionar_produto(nome, categoria, quantidade, preco, st.session_state.empresa_selecionada["empresa_id"])
                            st.success("Produto cadastrado!")
                        st.session_state.acao = None
                        st.rerun()
                    except mysql.connector.Error as err:
                        st.error(f"Erro no banco de dados: {err}")

    def show(self):
        st.title("Painel do Administrador")

        if 'empresa_selecionada' not in st.session_state or st.session_state.empresa_selecionada is None:
            st.header("1. Selecione uma empresa para gerenciar")
            empresas = self._carregar_empresas()
            # MODIFICADO: A chave do dicionário agora usa 'nome_fantasia' e 'empresa_id'
            opcoes = {f'{e["nome_fantasia"]} (ID: {e["empresa_id"]})': e for e in empresas}
            if not opcoes:
                st.warning("Nenhuma empresa (do tipo 'padrão' com perfil de empresa) encontrada para gerenciar.")
                return
            
            selecao = st.selectbox("Empresas Disponíveis", opcoes.keys())
            if st.button("Gerenciar Empresa"):
                st.session_state.empresa_selecionada = opcoes[selecao]
                st.rerun()
            return

        empresa = st.session_state.empresa_selecionada
        # MODIFICADO: Exibe o nome fantasia
        st.header(f"2. Gerenciando: {empresa['nome_fantasia']}")
        if st.button("← Trocar de Empresa"):
            st.session_state.empresa_selecionada = None
            st.session_state.acao = None
            st.rerun()
        
        st.markdown("---")

        if st.session_state.acao == 'cadastrar':
            self._mostrar_formulario_produto()
            if st.button("Cancelar"): st.session_state.acao = None; st.rerun()
        else:
            if st.button("✚ Cadastrar Novo Produto"):
                st.session_state.acao = 'cadastrar'
                st.rerun()
            
            # MODIFICADO: Passa o 'empresa_id' para carregar os produtos
            produtos = self._carregar_produtos_por_empresa(empresa["empresa_id"])
            if not produtos:
                st.info("Nenhum produto cadastrado para esta empresa.")
            
            for p in produtos:
                if st.session_state.acao == 'alterar' and st.session_state.produto_selecionado_id == p['id']:
                    self._mostrar_formulario_produto(p)
                    if st.button("Cancelar Alteração", key=f"cancel_edit_{p['id']}"): st.session_state.acao = None; st.rerun()
                else:
                    c1, c2, c3 = st.columns([3, 1, 1.2])
                    c1.write(f"**{p['nome']}**\n\n*ID do Produto: {p['id']}*")
                    c2.write(f"**Estoque:** {p['quantidade']}\n\n**Preço:** R$ {p['preco']:.2f}")
                    if c3.button("✏️ Alterar", key=f"edit_{p['id']}"):
                        st.session_state.acao = 'alterar'; st.session_state.produto_selecionado_id = p['id']; st.rerun()
                    if c3.button("🗑️ Excluir", key=f"del_{p['id']}"):
                        self._deletar_produto(p['id']); st.success(f"Produto '{p['nome']}' excluído!"); st.rerun()
                st.divider()

    def __del__(self):
        if hasattr(self, 'conn') and self.conn and self.conn.is_connected():
            self.cursor.close(); self.conn.close()