import streamlit as st
import sqlite3

# Conectar ao banco de dados SQLite
def create_connection():
    conn = sqlite3.connect("users.db")
    return conn

# Criar tabela de usuários
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        is_admin INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# Inserir usuário
def insert_user(username, password, is_admin=0):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, password, is_admin))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Usuário já existe!")
    conn.close()

# Verificar login
def check_login(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Criar tabela ao iniciar
def initialize_db():
    create_table()
    # Criar admin se não existir
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = 'nicolas'")
    if not cursor.fetchone():
        insert_user("nicolas", "123", is_admin=1)
    conn.close()

initialize_db()

# Interface Streamlit
st.title("Sistema de Login com SQLite")

menu = ["Login", "Registrar"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        user = check_login(username, password)
        if user:
            st.success(f"Bem-vindo, {username}!")
            if user[0] == 1:
                st.info("Você está logado como administrador.")
        else:
            st.error("Usuário ou senha incorretos!")

elif choice == "Registrar":
    st.subheader("Registrar Novo Usuário")
    new_user = st.text_input("Novo Usuário")
    new_pass = st.text_input("Nova Senha", type="password")
    if st.button("Registrar"):
        insert_user(new_user, new_pass)
        st.success("Usuário registrado com sucesso! Agora você pode fazer login.")

