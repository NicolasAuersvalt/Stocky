from entidade import Entidade
from estoque import Estoque

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
