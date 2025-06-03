import streamlit as st
import mysql.connector
import hashlib

from header import *
from page.estoque import *
from page.main import *
from page.estoque import *
from dotenv import load_dotenv
import os


class Pages():
    def conectar():
        return mysql.connector.connect (
           host=st.secrets["mysql"]["host"],
           user=st.secrets["mysql"]["user"],
           password=st.secrets["mysql"]["password"],
           database=st.secrets["mysql"]["database"]
        )
    
    def verificar_usuario(email: str, senha: str):
        conn = conectar()
        cursor = conn.cursor()
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha_hash))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario
    
    def cadastrar_usuario(nome: str, email: str, senha: str):
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