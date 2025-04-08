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
    st.write(f"**{nome}**")
    st.write(f"- **Mentor:** {mentor}")
    st.write(f"- **Projetos:** {projetos}")

    col1, col2 = st.columns(2)
    
    with col1:
        st.link_button("🔗 Linkedin", linkedin)

    with col2:
        st.link_button("🐙 Portfólio", github)
    
    st.markdown("---")

def inicio():
    st.title("Bem-vindo ao Laboratório Lambda")

    # Exibir a imagem principal
    imagem_path = "assets/LambdaLabs.png"
    st.image(imagem_path, width=400)

    # Exibir mensagem inicial
    st.write(dados['mensagem_inicial'])
    st.markdown("---")

    # Pesquisador Principal
    exibir_pesquisador(
        dados['pesquisador_principal'],
        dados['mentor_principal'],
        dados['projetos_principal'],
        dados['linkedin_principal'],
        dados['portfolio_principal']
    )

    # Pesquisador Associado
    associado = dados['pesquisador_associado']
    exibir_pesquisador(
        associado['nome'],
        associado['mentor'],
        associado['projetos'],
        "https://www.linkedin.com/in/gabriel-trevisani-a811131b5/",
        "https://github.com/fermathematician"
    )

    # Pesquisador Assistente
    assistente = dados['pesquisador_assistente']
    exibir_pesquisador(
        assistente['nome'],
        assistente['mentor'],
        assistente['projetos'],
        "https://www.linkedin.com/in/pedro-nascimento-4a35982b0/",
        "https://github.com/nascpedro"
    )

    # Exibir o Revisor
    st.write(f"**Revisor:** {dados['revisor']}")
    st.markdown("---")
