import mysql.connector
import streamlit as st
import hashlib
#from src.Entidades.administrador import Administrador
#from src.Entidades.empresa import Empresa

from src.geral import *

def conectar():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
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

def cadastrar_usuario(nome, email, senha, tipo):
    conn = conectar()
    cursor = conn.cursor()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)",
                       (nome, email, senha_hash, tipo))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("Erro:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def fazer_login(email, senha):
    usuario = verificar_usuario(email, senha)
    if usuario:
        id, nome, email, senha_db, tipo = usuario
        if tipo == "administrador":
            return Administrador(nome, email, senha_db, id)
        elif tipo == "empresa":
            return Empresa(nome, email, senha_db, id)
    return None
