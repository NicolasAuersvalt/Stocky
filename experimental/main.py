from usuario import Usuario
from empresa import Empresa
from administrador import Administrador

usuario = Usuario("Nicolas", "nicolasauersvalt@gmail.com", "123", "1", "utfpr")
print(usuario.showInfo())

empresa = Empresa("Utfpr", "utfpr@gmail.com", "213", "2", "utfpr")
print(empresa.showInfo())

adm = Administrador("Everton", "everton@gmail.com", "223", "3", "utfpr")
print(adm.showInfo())