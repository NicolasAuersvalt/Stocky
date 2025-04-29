from usuario import Usuario
from empresa import Empresa
from administrador import Administrador

usuario = Usuario("Nicolas", "nicolasauersvalt@gmail.com", "123", "1")
print(usuario.showInfo())

empresa = Empresa("Utfpr", "utfpr@gmail.com", "213", "2")
print(empresa.showInfo())

adm = Administrador("Everton", "everton@gmail.com", "223", "3")
print(adm.showInfo())

usuario.setEmpresa(empresa)
print(usuario.showInfo())