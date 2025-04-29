from entidade import Entidade

class Administrador(Entidade):

    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        super().__init__(_nome, _email, _senha, _id)
        self.empresa = None

    def setEmpresa(self, _empresa):
        empresa = _empresa

    def getEmpresa(self):
        return empresa

    def showInfo(self) -> None:
        print("Id: {}".format(self.getId()))
        print("Nome: {}".format(self.getName()))
        print("Email: {}".format(self.getEmail()))
        if(self.empresa==None):
            print("Não é associado a nenhuma empresa!")
        else:
            print(getEmpresa().getName())