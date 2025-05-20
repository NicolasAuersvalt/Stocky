from usuario import Usuario
from empresa import Empresa

class Vendedor(Usuario):
    def __init__(self, _nome: str, _email: str, _senha: str, _id: str):
        super().__init__(_nome, _email, _senha, _id)
        self.produtos = []  # produtos vendidos pelo vendedor, se quiser usar depois
        self.empresa = None

    def get_vendas(self):
        return self.produtos  # ou implementar uma contagem de vendas se quiser

    def set_empresa(self, _empresa: Empresa):
        self.empresa = _empresa

    def vender(self, tipo: str, qtd: int = 1):
        if self.empresa:
            estoque = self.empresa.procurarEstoque(tipo)
            if estoque and estoque.getQuantidade() >= qtd:
                self.empresa.vender(tipo, qtd)
                self.produtos += [tipo] * qtd  # registra o tipo vendido
            else:
                print("Erro: estoque insuficiente ou não encontrado.")
        else:
            print("Erro: nenhuma empresa associada.")


