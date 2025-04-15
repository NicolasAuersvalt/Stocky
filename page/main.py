import streamlit as st
import json
import os
import webbrowser

text_path = os.path.join('assets', 'textos', 'main.json')

# Carregar os dados do arquivo JSON
with open(text_path, 'r', encoding='utf-8') as f:
    dados = json.load(f)

    # Função para exibir informações dos pesquisadores
def exibir_pesquisador(nome, mentor, projetos, linkedin, github):

    col1, col2 = st.columns(2)
    
    st.markdown("---")

def inicio():
    
    st.title("Bem-vindo ao Laboratório Lambda")

    # Exibir a imagem principal
    imagem_path = "assets/LambdaLabs.png"
    st.image(imagem_path, width=400)

    # Exibir mensagem inicial
    st.write(dados['mensagem_inicial'])
    st.markdown("---")

    st.markdown("---")
