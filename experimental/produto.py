class Produto:
    def __init__(self, id:str, tipo:str):
        self.id = id
        self.tipo = tipo
    
    def getId(self):
        return self.id
    
    def getTipo(self):
        return self.tipo

    