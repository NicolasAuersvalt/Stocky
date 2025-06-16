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
        O construtor da classe.
        """
        pass

    @staticmethod
    def _conectar():
        """
        Método estático e privado para conectar ao banco de dados.
        """
        return mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )

    def verificar_usuario(self, email: str, senha: str):
        """
        Verifica as credenciais e busca os dados do usuário e da empresa associada.
        """
        conn = self._conectar()
        cursor = conn.cursor(dictionary=True)
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        # --- CONSULTA SQL ALTERADA ---
        # Usamos um LEFT JOIN para buscar o 'empresa_id' da tabela 'empresas'
        # com base no 'id' do usuário encontrado.
        sql_query = """
            SELECT u.id, u.nome, u.tipo, e.id AS empresa_id
            FROM usuarios u
            LEFT JOIN empresas e ON u.id = e.usuario_id
            WHERE u.email = %s AND u.senha = %s
        """
        
        cursor.execute(sql_query, (email, senha_hash))
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return usuario

    def cadastrar_usuario(self, nome: str, email: str, senha: str, tipo: str):
        """
        Cadastra um novo usuário e, se for do tipo 'padrão', cria uma empresa associada.
        Tudo dentro de uma transação para garantir a integridade.
        """
        conn = self._conectar()
        cursor = conn.cursor()
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        try:
            # Inicia uma transação
            conn.start_transaction()

            # 1. Insere o novo usuário na tabela 'usuarios'
            sql_insert_usuario = "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_insert_usuario, (nome, email, senha_hash, tipo.lower()))
            
            # Pega o ID do usuário que acabamos de criar
            novo_usuario_id = cursor.lastrowid

            # 2. Se o usuário for do tipo 'padrão', cria uma empresa para ele
            if tipo.lower() == 'padrão':
                # O nome fantasia pode ser genérico inicialmente ou vir de outro campo do formulário
                nome_fantasia_empresa = f"Empresa de {nome}" 
                sql_insert_empresa = "INSERT INTO empresas (usuario_id, nome_fantasia) VALUES (%s, %s)"
                cursor.execute(sql_insert_empresa, (novo_usuario_id, nome_fantasia_empresa))

            # 3. Se tudo correu bem, salva as alterações no banco
            conn.commit()
            return True
            
        except mysql.connector.Error as e:
            # Se algo der errado, desfaz tudo
            conn.rollback()
            print(f"Erro ao cadastrar usuário: {e}")
            return False
        finally:
            cursor.close()
            conn.close()