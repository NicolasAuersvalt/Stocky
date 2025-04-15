import streamlit as st
import json
import os
import webbrowser

text_path = os.path.join('assets', 'textos', 'main.json')

# Carregar os dados do arquivo JSON
with open(text_path, 'r', encoding='utf-8') as f:
    dados = json.load(f)

class Estoque:
    def __init__(self, input_str):
        self.input = input_str.replace(' ', '')

        pass

    def estoque():

        st.title("Bem-vindo ao Stocky")

        # Exibir mensagem inicial
        st.write(dados['mensagem_inicial'])
        st.markdown("---")