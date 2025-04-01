import streamlit as st
import sqlite3

# Função para conectar ao banco de dados
def create_connection():
    conn = sqlite3.connect('usuarios.db')
    return conn

# Função para verificar as credenciais de login
def check_login(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Função para registrar um novo usuário
def register_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        st.success('Usuário registrado com sucesso!')
    except sqlite3.IntegrityError:
        st.error('Erro: Nome de usuário já existe.')
    conn.close()

# Interface do usuário
st.title('Sistema de Login com Streamlit e SQLite')

menu = ['Login', 'Registrar']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Login':
    st.subheader('Página de Login')
    username = st.text_input('Nome de usuário')
    password = st.text_input('Senha', type='password')
    if st.button('Entrar'):
        user = check_login(username, password)
        if user:
            st.success(f'Bem-vindo, {username}!')
            if user[3] == 1:
                st.info('Você é um administrador.')
        else:
            st.error('Nome de usuário ou senha incorretos.')

elif choice == 'Registrar':
    st.subheader('Página de Registro')
    new_username = st.text_input('Novo nome de usuário')
    new_password = st.text_input('Nova senha', type='password')
    if st.button('Registrar'):
        register_user(new_username, new_password)

