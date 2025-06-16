# credenciais.py

import streamlit as st
# A importação da CLASSE específica do módulo.
from src.Gerenciadores.gerenciadorLogin import GerenciadorLogin

class CredentialsPage:
    
    def __init__(self):
        """
        Ao criar a página de credenciais, também criamos uma instância
        do nosso gerenciador de login para usar em toda a classe.
        """
        # Criamos uma instância do gerenciador.
        self.gerenciador = GerenciadorLogin()

    def tela_login(self):
        st.subheader("Acessar o Sistema")
        
        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar", key="login_button"):
            if not email or not senha:
                st.warning("Por favor, preencha o email e a senha.")
                return

            # ---- ALTERAÇÃO IMPORTANTE AQUI ----
            # Garanta que este método retorne um dicionário com 'id' e 'empresa_id'
            usuario = self.gerenciador.verificar_usuario(email, senha)
            
            if usuario:
                # Salva todas as informações necessárias na sessão
                st.session_state['logado'] = True
                st.session_state['usuario_nome'] = usuario['nome']
                st.session_state['usuario_tipo'] = usuario['tipo']
                
                # ====> LINHAS ADICIONADAS <====
                # Estas são as novas linhas essenciais para a página de estoque
                st.session_state['usuario_id'] = usuario['id']
                st.session_state['empresa_id'] = usuario['empresa_id'] # Ajuste o nome da chave se for diferente

                st.success(f"Login bem-sucedido! Bem-vindo(a), {usuario['nome']}!")
                st.rerun()
            else:
                st.error("Email ou senha inválidos.")

    def tela_cadastro(self):
        st.subheader("Cadastro de Novo Usuário")

        nome = st.text_input("Nome completo", key="cad_nome")
        email = st.text_input("Email", key="cad_email")
        # Ajustado para usar os mesmos valores do ENUM do banco de dados ('padrão', 'admin')
        tipo = st.selectbox("Tipo de Usuário", ["padrão", "admin"], key="cad_tipo")
        senha = st.text_input("Senha", type="password", key="cad_senha")
        senha2 = st.text_input("Confirme a senha", type="password", key="cad_senha2")

        if st.button("Cadastrar", key="cad_button"):
            if senha != senha2:
                st.warning("As senhas não coincidem!")
            elif not all([nome, email, senha, tipo]):
                st.warning("Preencha todos os campos obrigatórios.")
            else:
                # Usamos o método da instância do gerenciador aqui também.
                sucesso = self.gerenciador.cadastrar_usuario(nome, email, senha, tipo)
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