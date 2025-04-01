import streamlit as st
import mysql.connector
import hashlib

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="seu_usuario",
        password="sua_senha",
        database="seu_banco"
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL
                      )''')
    conn.commit()
    cursor.close()
    conn.close()

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hash_password(password)))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user and user[0] == hash_password(password):
        return True
    return False

def main():
    st.title("Sistema de Login")
    menu = ["Login", "Cadastro"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    create_users_table()
    
    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if login_user(username, password):
                st.success(f"Bem-vindo, {username}!")
            else:
                st.error("Usuário ou senha incorretos")
    
    elif choice == "Cadastro":
        st.subheader("Cadastro de Usuário")
        new_user = st.text_input("Usuário")
        new_password = st.text_input("Senha", type="password")
        if st.button("Cadastrar"):
            if register_user(new_user, new_password):
                st.success("Usuário cadastrado com sucesso! Agora você pode fazer login.")
            else:
                st.error("Usuário já existe. Escolha outro nome.")

if __name__ == "__main__":
    main()

