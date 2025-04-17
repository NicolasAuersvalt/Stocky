from abc import ABC
import estoque

class Usuario(ABC):
    def __init__(self, nome: str, idd: str, empresa, est: estoque.Estoque):
        self.name = nome
        self.id = idd
        self.empresaassociada = empresa
        self.estoque = est
    
    #def testao(self):#
     # print("Passou")#

    def getId(self):
        return self.id
        