from produto import Produto
import numpy as np 

class Estoque():
    def __init__(self, _id: str, _tipo: str):
        super().__init__()
        self.id = _id # Id do estoque (Ex: estoque bebidas: 151)
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

        self.estoque.reverse()

        for produto in self.estoque:
            self.preco += produto.getPreco()

