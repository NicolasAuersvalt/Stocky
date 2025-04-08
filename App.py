from header import *
from page.pageGrafo import *
from page.pageGrafica import *
from page.pagePolinomio import *
from page.pageCifra import *
from page.main import *


def main():
    # Menu lateral para selecionar páginas
    menu = ["Início", "Computação Gráfica", "Busca de Caminhos em Grafo", "Criptografia", "Polinômios"]
    escolha = st.sidebar.selectbox("Escolha a página:", menu)
    
    if escolha == "Início":
        inicio()
    
    elif escolha == "Computação Gráfica":
        pagina_operacoes()
    elif escolha == "Busca de Caminhos em Grafo":
        pagina_grafo()
    elif escolha == "Criptografia":
        pagina_cifra()
    elif escolha == "Polinômios":
        pagina_polinomios()

if __name__ == "__main__":
    main()
