from abc import ABC, abstractmethod

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

class Produto:
    def __init__(self, _id: str, _tipo: str, _preco: int, _nome:str, _categoria:str):
        self.id = _id
        self.tipo = _tipo
        self.preco = _preco
        self.nome = _nome
        self.categoria = _categoria

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

class Estoque:
    def __init__(self, _id: str, _tipo: str):
        self.id = _id
        self.tipo = _tipo
        self.estoque = []

    def inserirProduto(self, _produto: Produto):
        if _produto.getTipo() == self.tipo:
            self.estoque.append(_produto)
        else:
            print("Erro: Tipo do produto não é o mesmo do estoque")

    def getTipo(self):
        return self.tipo

    def getPreco(self):
        return sum(produto.getPreco() for produto in self.estoque)

    def getQuantidade(self):
        return len(self.estoque)

    def removerProdutos(self, qtd: int):
        if qtd <= len(self.estoque):
            for _ in range(qtd):
                self.estoque.pop()
            return True
        else:
            print("Erro: quantidade insuficiente no estoque")
            return False

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

    def getVendas(self):
        return self.produtos  # ou implementar uma contagem de vendas se quiser

    def setEmpresa(self, _empresa: Empresa):
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



esq = Estoque("1", "2313")

prod1 = Produto("2", "0000", 10, "Vinho Tinto", "Bebida")
prod2 = Produto("3", "0000", 50, "Vinho Tinto Premium", "Bebida")
prod3 = Produto("4", "2313", 10, "Vinho Branco", "Bebida")

esq.inserirProduto(prod1)  # erro: tipo diferente (ignorado)
esq.inserirProduto(prod2)  # erro: tipo diferente (ignorado)
esq.inserirProduto(prod3)  # OK

print("Preço total do estoque:", esq.getPreco())  # Deve dar 10

empresa = Empresa("Utfpr", "utfpr@gmail.com", "213", "2")
empresa.inserirEstoque(esq)

vendedor = Vendedor("user", "vendedor.email@.com", "298365", "9174")
vendedor.setEmpresa(empresa)
vendedor.vender("2313")  # Vende um produto do estoque