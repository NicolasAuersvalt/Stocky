# App.py atualizado e corrigido

import streamlit as st
import os

# Os únicos imports necessários de nossas páginas/gerenciadores
from page.credenciais import CredentialsPage
from page.estoque import EstoquePage
from page.main import MainPage
from page.administrador import AdmPage

# ----- Função Principal -----

def main():
    """
    Função principal que atua como o roteador da aplicação.
    """
    st.set_page_config(page_title="Controle de Estoque", layout="wide")

    # Inicializa os estados da sessão se ainda não existirem
    # Usar .setdefault é uma boa prática para evitar erros na primeira execução
    st.session_state.setdefault("logado", False)
    st.session_state.setdefault("usuario_nome", None)
    st.session_state.setdefault("usuario_tipo", None)

    # --- ROTEADOR PRINCIPAL ---
    # Se o usuário não estiver logado, renderiza a página de credenciais.
    if not st.session_state["logado"]:
        # Cria uma instância da página de credenciais
        credential_page = CredentialsPage()
        # Chama o método que desenha a tela de login/cadastro
        credential_page.render()

    # Se o usuário estiver logado, mostra o conteúdo principal.
    else:
        st.sidebar.success(f"Logado como: {st.session_state['usuario_nome']}")
        
        # MODIFICAÇÃO PRINCIPAL: Verificação de tipo de usuário mais robusta
        # Com .strip() e .lower() para evitar erros de case ou espaços
        if st.session_state["usuario_tipo"].strip().lower() == "admin":
            # Se for admin, mostra a página de administração
            st.sidebar.markdown("---")
            st.sidebar.subheader("Painel de Controle")
            admin_page = AdmPage()
            admin_page.show()

        else: # Para qualquer outro tipo de usuário (ex: "Padrão")
            # Menu para os demais usuários
            menu = ["Início", "Estoque"]
            escolha = st.sidebar.selectbox("Escolha a página:", menu)

            if escolha == "Início":
                page = MainPage(
                    text_path=os.path.join("assets", "textos", "main.json"),
                    image_path=os.path.join("assets", "images", "logo_sem_fundo_texto.png")
                )
                page.show()

            elif escolha == "Estoque":
                page = EstoquePage(
                    text_path=os.path.join("assets", "textos", "main.json")
                )
                page.show()

        # Botão de sair fica na barra lateral para acesso constante
        if st.sidebar.button("Sair"):
            # Limpa toda a sessão para fazer logout
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()