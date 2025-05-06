import usuario
from usuario import Usuario
from empresa import Empresa

from typing import Dict


class Vendedor(Usuario):  # Use "Usuario" se estiver no mesmo arquivo
    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        super().__init__(_nome, _email, _senha, _id)
        self.produtos = []
        self.empresa = None 


    def GetVendas(self):
        return self.GetVendas

    def setEmpresa(self, _empresa: Empresa):
        self.empresa = _empresa

    def vender(self, tipo:str):
        empresa.vender(tipo)
