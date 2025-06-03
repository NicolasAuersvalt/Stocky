from abc import ABC, abstractmethod
import hashlib
import mysql.connector
import streamlit as st

# ---------- Entidades principais ----------

class Entidade(ABC):
    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        self.name = _nome
        self.id = _id
        self.email = _email
        self.senha = _senha

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def showInfo(self) -> None:
        print("Id: {}".format(self.getId()))
        print("Nome: {}".format(self.getName()))
        print("Email: {}".format(self.getEmail()))


class Administrador(Entidade):
    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        super().__init__(_nome, _email, _senha, _id)
        self.empresa = None

    def setEmpresa(self, _empresa):
        self.empresa = _empresa

    def getEmpresa(self):
        return self.empresa

    def showInfo(self) -> None:
        super().showInfo()
        if self.empresa is None:
            print("Não é associado a nenhuma empresa!")
        else:
            print("Empresa: {}".format(self.empresa.getName()))


class Empresa(Entidade):
    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        super().__init__(_nome, _email, _senha, _id)
        self.listaEstoque = []

    def inserirEstoque(self, _estoque):
        self.listaEstoque.append(_estoque)

    def setEstoque(self, _estoque):
        self.listaEstoque = _estoque

    def procurarEstoque(self, tipo: str):
        for est in self.listaEstoque:
            if est.getTipo() == tipo:
                return est
        return None

    def vender(self, _tipo: str):
        estoque = self.procurarEstoque(_tipo)
        if estoque:
            estoque.decrementar()

# ---------- Classes auxiliares ----------

class Produto:
    def __init__(self, _tipo: str, _preco: float):
        self.tipo = _tipo
        self.preco = _preco

    def getTipo(self):
        return self.tipo

    def getPreco(self):
        return self.preco


class Estoque:
    def __init__(self, _id: str, _tipo: str):
        self.id = _id
        self.tipo = _tipo
        self.preco = 0
        self.estoque = []

    def inserirProduto(self, _produto: Produto):
        if _produto.getTipo() == self.getTipo():
            self.estoque.append(_produto)
        else:
            print("Erro: Tipo do produto não é o mesmo do estoque")

    def getTipo(self):
        return self.tipo

    def getPreco(self):
        self.precoEstoque()
        return self.preco

    def precoEstoque(self):
        self.preco = sum(produto.getPreco() for produto in self.estoque)

    def decrementar(self):
        if self.estoque:
            self.estoque.pop()
        else:
            print("Estoque vazio.")

# ---------- Interface com o usuário ----------

class Pages:
    @staticmethod
    def conectar():
        return mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )

    @staticmethod
    def verificar_usuario(email: str, senha: str):
        conn = Pages.conectar()
        cursor = conn.cursor()
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha_hash))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

    @staticmethod
    def cadastrar_usuario(nome: str, email: str, senha: str, tipo: str):
        conn = Pages.conectar()
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


    @staticmethod
    def tela_cadastro():
        st.subheader("Cadastro de Novo Usuário")

        nome = st.text_input("Nome completo")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        senha2 = st.text_input("Confirme a senha", type="password")
        tipo = st.radio("Tipo de conta", ["empresa", "administrador"])

        if st.button("Cadastrar"):
            if senha != senha2:
                st.warning("As senhas não coincidem!")
            elif nome == "" or email == "" or senha == "":
                st.warning("Preencha todos os campos.")
            else:
                sucesso = Pages.cadastrar_usuario(nome, email, senha, tipo)
                if sucesso:
                    st.success("Usuário cadastrado com sucesso! Faça login.")
                else:
                    st.error("Erro ao cadastrar. Verifique se o email já está em uso.")

    def fazer_login():
        st.subheader("Login")

        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            usuario = Pages.verificar_usuario(email, senha)
            if usuario:
                id, nome, email, senha_db, tipo = usuario
                if tipo == "administrador":
                    st.session_state["usuario"] = Administrador(nome, email, senha_db, id)
                else:
                    st.session_state["usuario"] = Empresa(nome, email, senha_db, id)
                st.success(f"Bem-vindo, {nome} ({tipo})!")
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

