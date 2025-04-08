from header import *
from src.cifra import *
import json
import os


text_path = os.path.join('assets', 'textos', 'cifra.json')

# Carregar os dados do arquivo JSON
with open(text_path, 'r', encoding='utf-8') as f:
    dados = json.load(f)


def pagina_cifra():

    st.title("Criptografia por Cifra de Hill")

    opcoes = st.sidebar.selectbox("Escolha uma operação:", ["Teoria", "Cifras de Hill"])

    if opcoes == "Teoria":
        teoria()
    elif opcoes == "Cifras de Hill":
        cifra()


def teoria():
    st.write(dados['Introducao'])
    st.write(dados['Cifra'])

def cifra():
    cifra = Cifra()

    cifra.executar()
