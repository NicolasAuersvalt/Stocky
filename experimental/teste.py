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
        empresa = _empresa

    def getEmpresa(self):
        return empresa

    def showInfo(self) -> None:
        print("Id: {}".format(self.getId()))
        print("Nome: {}".format(self.getName()))
        print("Email: {}".format(self.getEmail()))
        if(self.empresa==None):
            print("Não é associado a nenhuma empresa!")
        else:
            print(getEmpresa().getName())


class Empresa(Entidade):
    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        super().__init__(_nome, _email, _senha, _id)
        self.listaEstoque = []

    def inserirEstoque(self, _estoque: Estoque):
        self.listaEstoque.append(_estoque)

    def setEstoque(self, _estoque):
        self.listaEstoque = _estoque

    def procurarEstoque(self, tipo: str):
        for item in self.listaEstoque:
            if item.getTipo() == tipo:
                return item
        return None

    def vender(self, _tipo: str, qtd: int = 1):
        item = self.procurarEstoque(_tipo)
        if item:
            sucesso = item.removerProdutos(qtd)
            if sucesso:
                print(f"{qtd} produto(s) do tipo '{_tipo}' vendidos.")
        else:
            print(f"Estoque do tipo '{_tipo}' não encontrado.")


class Vendedor(Usuario):
    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        super().__init__(_nome, _email, _senha, _id)
        self.produtos = []  # produtos vendidos pelo vendedor, se quiser usar depois
        self.empresa = None

    def get_vendas(self):
        return self.produtos  # ou implementar uma contagem de vendas se quiser

    def set_empresa(self, _empresa: Empresa):
        self.empresa = _empresa

    def vender(self, tipo: str, qtd: int = 1):
        if self.empresa:
            estoque = self.empresa.procurarEstoque(tipo)
            if estoque and estoque.getQuantidade() >= qtd:
                self.empresa.vender(tipo, qtd)
                self.produtos += [tipo] * qtd  # registra o tipo vendido
            else:
                print("Erro: estoque insuficiente ou não encontrado.")
        else:
            print("Erro: nenhuma empresa associada.")

class Produto:
    def __init__(self, _id: str, _tipo: str, _preco: int):
        self.id = _id
        self.tipo = _tipo
        self.preco = _preco

    def getId(self):
        return self.id

    def getTipo(self):
        return self.tipo

    def setPreco(self, _preco: int):
        if _preco > 0:
            self.preco = _preco
        else:
            print("Erro: valor inválido")

    def getPreco(self):
        return self.preco


class Usuario(Entidade):
    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        super().__init__(_nome, _email, _senha, _id)
        self.empresa = None

    def setEmpresa(self, empresa):
        self.empresa = empresa

    def getEmpresa(self):
        return self.empresa

    def showInfo(self) -> None:
        print("Id: {}".format(self.getId()))
        print("Nome: {}".format(self.getName()))
        print("Email: {}".format(self.getEmail()))

        if(self.empresa==None):
            print("Não é associado a nenhuma empresa!")
        else:
            print(self.getEmpresa().getName())
