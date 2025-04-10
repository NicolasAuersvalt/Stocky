import streamlit as st
import mysql.connector
import hashlib

from header import *
from page.pageGrafo import *
from page.pagePolinomio import *
from page.pageCifra import *
from page.main import *
from dotenv import load_dotenv
import os



# ----- Funções de Banco de Dados -----

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def verificar_usuario(email, senha):
    conn = conectar()
    cursor = conn.cursor()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha_hash))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

def cadastrar_usuario(nome, email, senha):
    conn = conectar()
    cursor = conn.cursor()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", 
                       (nome, email, senha_hash))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("Erro:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# ----- Função de Tela de Cadastro -----

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

# ----- Função Principal com Login e Menus -----

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

        menu = ["Início", "Computação Gráfica", "Busca de Caminhos em Grafo", "Criptografia", "Polinômios"]
        escolha = st.sidebar.selectbox("Escolha a página:", menu)

        if escolha == "Início":
            inicio()
        elif escolha == "Computação Gráfica":
            pagina_operacoes()
        elif escolha == "Busca de Caminhos em Grafo":
            pagina_grafo()
        elif escolha == "Criptografia":
            pagina_cifra()
        elif escolha == "Polinômios":
            pagina_polinomios()

        if st.sidebar.button("Sair"):
            st.session_state["logado"] = False
            st.rerun()

if __name__ == "__main__":
    main()
