import mysql.connector
import streamlit as st
import hashlib

class GerenciadorLogin:
    @staticmethod
    def _conectar():
        return mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )

    def verificar_usuario(self, email: str, senha: str):
        """Verifica as credenciais e busca os dados do usuário, incluindo empresa_id."""
        conn = self._conectar()
        cursor = conn.cursor(dictionary=True)
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        # --- CONSULTA ALTERADA ---
        # Não precisa mais de JOIN. Pega tudo da tabela de usuários.
        sql_query = "SELECT id, nome, tipo, empresa_id FROM usuarios WHERE email = %s AND senha = %s"
        cursor.execute(sql_query, (email, senha_hash))
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return usuario

    # --- MÉTODO ALTERADO ---
    # Agora recebe 'empresa_id' e não cria mais uma empresa automaticamente.
    def cadastrar_usuario(self, nome: str, email: str, senha: str, tipo: str, empresa_id: int):
        """Cadastra um novo usuário associando a uma empresa existente."""
        conn = self._conectar()
        cursor = conn.cursor()
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        try:
            # A query agora inclui o empresa_id.
            sql_insert_usuario = "INSERT INTO usuarios (nome, email, senha, tipo, empresa_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_insert_usuario, (nome, email, senha_hash, tipo.lower(), empresa_id))
            conn.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao cadastrar usuário: {e}")
            return False
        finally:
            cursor.close()
            conn.close()