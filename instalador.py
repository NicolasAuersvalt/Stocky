import subprocess
import sys

# Lista dos pacotes que você deseja instalar
pacotes = ["streamlit", "numpy", "plotly", "networkx", "matplotlib"]

# Função para instalar pacotes
def instalar_pacotes():
    for pacote in pacotes:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

# Executar a função
if __name__ == "__main__":
    instalar_pacotes()
    print("Todos os pacotes foram instalados com sucesso.")
