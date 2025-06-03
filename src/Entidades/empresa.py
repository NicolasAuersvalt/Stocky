from src.Entidades.entidade import Entidade
from src.estoque import Estoque

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



    
        

        
