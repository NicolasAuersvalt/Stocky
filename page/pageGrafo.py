from header import *
from src.grafo import *
import json
import os


text_path = os.path.join('assets', 'textos', 'grafo.json')

# Carregar os dados do arquivo JSON
with open(text_path, 'r', encoding='utf-8') as f:
    dados = json.load(f)


def pagina_grafo():

    st.title("Grafos")

    opcoes = st.sidebar.selectbox("Escolha uma operação:", ["Teoria", "Menor Caminho"])

    if opcoes == "Teoria":
        teoria()
    elif opcoes == "Menor Caminho":
        caminho()


def teoria():
    st.write(dados['Grafos'])

def caminho():
    grafo = Grafo()
    grafo.executar()

