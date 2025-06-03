import streamlit as st
import mysql.connector
import hashlib
import os

from src.Gerenciadores.gerenciadorLogin import *
from page.estoque import *
from page.main import *

def tela_cadastro():
    st.subheader("Cadastro de Novo Usuário")

    nome = st.text_input("Nome completo")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    senha2 = st.text_input("Confirme a senha", type="password")

    if st.button("Cadastrar"):
        if senha != senha2:
            st.warning("As senhas não coincidem!")
        elif nome == "" or email == "" or senha == "":
            st.warning("Preencha todos os campos.")
        else:
            sucesso = cadastrar_usuario(nome, email, senha)
            if sucesso:
                st.success("Usuário cadastrado com sucesso! Faça login.")
            else:
                st.error("Erro ao cadastrar. Verifique se o email já está em uso.")

# ----- Função Principal -----

def main():
    st.set_page_config(page_title="Projeto com Login", layout="wide")

    if "logado" not in st.session_state:
        st.session_state["logado"] = False

    if not st.session_state["logado"]:
        st.title("Autenticação")

        opcao = st.radio("Escolha uma opção:", ["Login", "Cadastro"])

        if opcao == "Login":
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")

            if st.button("Entrar"):
                usuario = verificar_usuario(email, senha)
                if usuario:
                    st.session_state["logado"] = True
                    st.session_state["usuario"] = usuario[1]  # nome
                    st.success(f"Bem-vindo, {usuario[1]}!")
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")
        
        elif opcao == "Cadastro":
            tela_cadastro()

    else:
        st.sidebar.success(f"Logado como: {st.session_state['usuario']}")

        menu = ["Estoque", "Info"]
        escolha = st.sidebar.selectbox("Escolha a página:", menu)

        if escolha == "Info":
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

        if st.sidebar.button("Sair"):
            st.session_state["logado"] = False
            st.rerun()

if __name__ == "__main__":
    main()
