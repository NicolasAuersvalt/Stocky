from entidade import Entidade
from estoque import Estoque

class Empresa(Entidade):

    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        super().__init__(_nome, _email, _senha, _id)
        self.estoque = None
        
    def setEstoque(_estoque):
        self.estoque = _estoque
        

        
