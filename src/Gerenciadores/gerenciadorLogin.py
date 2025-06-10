# src/Gerenciadores/gerenciadorLogin.py

import mysql.connector
import streamlit as st
import hashlib

class GerenciadorLogin:
    """
    Classe que encapsula toda a lógica de interação com o banco de dados
    para autenticação e cadastro de usuários.
    """

    def __init__(self):
        """
        O construtor da classe. No futuro, poderia ser usado para inicializar
        um pool de conexões, por exemplo.
        """
        pass

    @staticmethod
    def _conectar():
        """
        Método estático e privado para conectar ao banco de dados.
        Não precisa de 'self' pois não acessa dados da instância.
        """
        return mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )

    def verificar_usuario(self, email: str, senha: str):
        """
        Verifica as credenciais do usuário no banco de dados.
        Agora é um método da classe.
        """
        conn = self._conectar()
        cursor = conn.cursor(dictionary=True)
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha_hash))
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return usuario

    def cadastrar_usuario(self, nome: str, email: str, senha: str, tipo: str):
        """
        Cadastra um novo usuário no banco de dados.
        Agora é um método da classe.
        """
        conn = self._conectar()
        cursor = conn.cursor()
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        try:
            cursor.execute("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)",
                           (nome, email, senha_hash, tipo))
            conn.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao cadastrar usuário: {e}")
            return False
        finally:
            cursor.close()
            conn.close()