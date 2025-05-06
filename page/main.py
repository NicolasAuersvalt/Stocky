# main.py

import streamlit as st
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

# Classe abstrata base
class Page(ABC):
    @abstractmethod
    def show(self):
        pass

# Classe da página principal
class MainPage(Page):
    def __init__(self, text_path: str, image_path: str):
        self.text_path = Path(text_path)
        self.image_path = Path(image_path)
        self.dados = self._load_data()

    def _load_data(self):
        """Carrega os dados do JSON."""
        with open(self.text_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def show(self):
        """Renderiza a página principal no Streamlit."""
        #st.title("Bem-vindo, usuário")

        # Exibe a imagem principal
        if self.image_path.exists():
            st.image(str(self.image_path), width=400)
        else:
            st.warning("Imagem não encontrada.")

        # Exibe mensagem inicial
        mensagem = self.dados.get('mensagem_inicial', '')
        st.write(mensagem)

        st.markdown("---")

        # Exibir pesquisadores, se existirem
        pesquisadores = self.dados.get('pesquisadores', [])
        for p in pesquisadores:
            self._exibir_pesquisador(p)

    def _exibir_pesquisador(self, pesquisador: dict):
        """Exibe os dados de um pesquisador."""
        nome = pesquisador.get('nome', 'Nome não informado')
        mentor = pesquisador.get('mentor', 'Mentor não informado')
        projetos = pesquisador.get('projetos', [])
        linkedin = pesquisador.get('linkedin', '#')
        github = pesquisador.get('github', '#')

        col1, col2 = st.columns(2)
        with col1:
            st.subheader(nome)
            st.write(f"**Mentor:** {mentor}")
            st.write("**Projetos:**")
            for proj in projetos:
                st.markdown(f"- {proj}")
        with col2:
            st.markdown(f"[LinkedIn]({linkedin})")
            st.markdown(f"[GitHub]({github})")

        st.markdown("---")


# Ponto de entrada
def main():
    text_path = os.path.join('assets', 'textos', 'main.json')
    image_path = os.path.join('assets', 'images', 'logo_sem_fundo_texto.png')
    
    page = MainPage(text_path=text_path, image_path=image_path)
    page.show()


if __name__ == "__main__":
    main()
