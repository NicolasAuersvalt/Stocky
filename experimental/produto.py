class Produto:
    def __init__(self, _id: str, _tipo: str, _preco: int, _nome:str, _categoria:str):
        self.id = _id
        self.tipo = _tipo
        self.preco = _preco
        self.nome = _nome
        self.categoria = _categoria

    def getId(self):
        return self.id

    def getTipo(self):
        return self.tipo

    def setPreco(self, _preco: int):
        if _preco > 0:
            self.preco = _preco
        else:
            print("Erro: valor inválido")

    def getPreco(self):
        return self.preco
    
    def 
