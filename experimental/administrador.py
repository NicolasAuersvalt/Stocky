import Usuario

class Administrador(Usuario):
    def __init__(self, nome: str, idd: str, est: Usuario.estoque.Estoque):
       super().__init__(nome, idd, est)
    
    
    
