import usuario
import Produto
from typing import Dict


class Vendedor(usuario.Usuario):
    def __init__(self, nome: str, idd: str, est: usuario.estoque.Estoque, Produtos:Dict[Produto.Produto, int] ):
       super().__init__(nome, idd, est)
       self.Produtos = Produtos

    def teste():
        print("ALO")

    def ContabilizaVendas(self, Prod: Produto.Produto, qnt: int):
        self.QntVendas+= qnt
    
        if(Prod in self.produtos):
            self.produtos[Prod]-=qnt
    
        else:
            print("Produto não encontrado.")
    
    #def ComprarProdutos(self, Prod, qnt):

    def GetVendas(self):
        return self.GetVendas

    #def GetCompras(self):
    #    return self.compras