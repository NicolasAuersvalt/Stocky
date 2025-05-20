from produto import Produto

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
