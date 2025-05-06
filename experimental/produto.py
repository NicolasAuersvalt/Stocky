#from abc import ABC, abstractmethod

class Produto():
    def __init__(self, _id:str, _tipo:str, _preco:int):
        self.id = _id
        self.tipo = _tipo
        self.preco = _preco
    
    def getId(self):
        return self.id
    
    def getTipo(self):
        return self.tipo

    def setPreco(self, _preco:int):
        if(_preco>0):
            self.preco = _preco
        else:
            print("Erro: valor inválido")

    def getPreco(self):
        return self.preco

    