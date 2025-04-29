
from abc import ABC, abstractmethod

class Entidade(ABC):

    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        self.name = _nome
        self.id = _id
        self.email = _email
        self.senha = _senha

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def showInfo(self) -> None:
        print("Id: {}".format(self.getId()))
        print("Nome: {}".format(self.getName()))
        print("Email: {}".format(self.getEmail()))

