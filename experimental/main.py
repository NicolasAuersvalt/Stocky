from usuario import Usuario
from empresa import Empresa
from administrador import Administrador
from estoque import Estoque
from vendedor import Vendedor
from produto import Produto

"""
usuario = Usuario("Nicolas", "nicolasauersvalt@gmail.com", "123", "1")
print(usuario.showInfo())


print(empresa.showInfo())

adm = Administrador("Everton", "everton@gmail.com", "223", "3")
print(adm.showInfo())

usuario.setEmpresa(empresa)
print(usuario.showInfo())

"""
esq = Estoque(1, 2313) # vinho

# 0000 - vinho
# 0020 - vinho branco
prod1 = Produto(2, 0000, 10) 
prod2 = Produto(3, 0000, 50)
prod3 = Produto(4, 2313, 10)

esq.inserirProduto(prod1)
esq.inserirProduto(prod2)
esq.inserirProduto(prod3)

print(esq.getPreco())

usuario = Usuario("Nicolas", "nicolasauersvalt@gmail.com", "123", "1")
empresa = Empresa("Utfpr", "utfpr@gmail.com", "213", "2")

usr = Vendedor("user","usr.email@.com", "298365", "9174")

usr.vender(0000)


'''
prod = Produto(10, 15, 100)
prod.setPreco(500)
print(prod.getPreco())
'''

