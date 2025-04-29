from entidade import Entidade

class Empresa(Entidade):

    def __init__(self, _nome: str, _email: str, _senha: str, _id: str, _empresa):
        super().__init__(_nome, _email, _senha, _id, _empresa)
        #self.empresa = tipo_objeto_empresa
        self.empresa = _empresa

