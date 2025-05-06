from entidade import Entidade
from estoque import Estoque

class Empresa(Entidade):

    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        super().__init__(_nome, _email, _senha, _id)
        self.listaEstoque = []

    def inserirEstoque(self, _estoque: Estoque):
        self.estoque.append(_estoque)
        
    def setEstoque(self, _estoque):
        self.estoque = _estoque

    def procurarEstoque(self, tipo:str):
        if()0000000000000000000000000

    def vender(self, _tipo:str):
        if(self.procurarEstoque(_tipo))
            self.decrementar()

    def decrementar(self):
        if listaEstoque



    
        

        
