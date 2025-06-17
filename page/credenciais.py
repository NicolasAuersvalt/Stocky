import streamlit as st
from src.Gerenciadores.gerenciadorLogin import GerenciadorLogin

class CredentialsPage:
    def __init__(self):
        self.gerenciador = GerenciadorLogin()

    def _carregar_empresas(self):
        """Função auxiliar para buscar as empresas para o menu de seleção."""
        conn = self.gerenciador._conectar()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT id, nome_fantasia FROM empresas ORDER BY nome_fantasia")
                return cursor.fetchall()
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        return []

    def tela_login(self):
        # (Esta função não precisa de alterações)
        st.subheader("Acessar o Sistema")
        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")
        if st.button("Entrar", key="login_button"):
            if not email or not senha:
                st.warning("Por favor, preencha o email e a senha."); return
            usuario = self.gerenciador.verificar_usuario(email, senha)
            if usuario:
                st.session_state['logado'] = True
                st.session_state['usuario_nome'] = usuario['nome']
                st.session_state['usuario_tipo'] = usuario['tipo']
                st.session_state['usuario_id'] = usuario['id']
                st.session_state['empresa_id'] = usuario['empresa_id']
                st.success(f"Login bem-sucedido! Bem-vindo(a), {usuario['nome']}!")
                st.rerun()
            else:
                st.error("Email ou senha inválidos.")

    def tela_cadastro(self):
        st.subheader("Cadastro de Novo Usuário")
        
        # --- ALTERAÇÃO PRINCIPAL AQUI ---
        # Busca a lista de empresas para o usuário selecionar
        empresas = self._carregar_empresas()
        if not empresas:
            st.error("Nenhuma empresa cadastrada no sistema. Contate um administrador.")
            return

        # Cria um dicionário para o selectbox: 'Nome da Empresa' -> id_da_empresa
        opcoes_empresa = {emp['nome_fantasia']: emp['id'] for emp in empresas}
        
        # Adiciona o campo de seleção de empresa ao formulário
        empresa_selecionada_nome = st.selectbox("Selecione a Empresa", options=opcoes_empresa.keys())
        empresa_selecionada_id = opcoes_empresa[empresa_selecionada_nome]

        nome = st.text_input("Nome completo", key="cad_nome")
        email = st.text_input("Email", key="cad_email")
        tipo = st.selectbox("Tipo de Usuário", ["padrão"], key="cad_tipo", disabled=True) # Assume que só usuários padrão são cadastrados aqui
        senha = st.text_input("Senha", type="password", key="cad_senha")
        senha2 = st.text_input("Confirme a senha", type="password", key="cad_senha2")

        if st.button("Cadastrar", key="cad_button"):
            if senha != senha2:
                st.warning("As senhas não coincidem!")
            elif not all([nome, email, senha, empresa_selecionada_id]):
                st.warning("Preencha todos os campos obrigatórios.")
            else:
                # Agora passamos o ID da empresa selecionada para o gerenciador
                sucesso = self.gerenciador.cadastrar_usuario(nome, email, senha, "padrão", empresa_selecionada_id)
                if sucesso:
                    st.success("Usuário cadastrado com sucesso! Agora você pode fazer login.")
                else:
                    st.error("Erro ao cadastrar. O email fornecido já pode estar em uso.")

    def render(self):
        st.title("🔐 Autenticação")
        escolha = st.sidebar.radio("Navegação", ["Login", "Cadastrar"])
        if escolha == "Login":
            self.tela_login()
        elif escolha == "Cadastrar":
            self.tela_cadastro()