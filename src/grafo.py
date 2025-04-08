import numpy as np
import networkx as nx
import streamlit as st
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self):
        self.camI = None
        self.camJ = None
        self.grafo_input = None
        self.edges = None
        self.mat = None
        self.apoio = None
        self.final = None
        self.len_mat = None

    def obter_entradas(self):
        # Entradas do usuário
        self.camI = st.number_input("Valor de partida (nó inicial)", min_value=1, step=1)
        self.camJ = st.number_input("Valor de destino (nó final)", min_value=1, step=1)
        
        # Entrada do grafo
        self.grafo_input = st.text_area("Insira o grafo (ex: '1 2\\n1 3\\n3 2')", 
                                        "1 2\n1 3\n3 2\n2 5\n5 6\n6 7\n5 9\n9 7\n2 4\n4 8\n8 11\n8 10\n8 9\n3 10\n4 5")

        # Processar a entrada do grafo
        self.edges = [list(map(int, line.split())) for line in self.grafo_input.strip().split('\n')]

    def processar_grafo(self):
        if not self.edges:
            st.error("Por favor, insira pelo menos uma aresta no grafo.")
            return
        
        # Determinar o tamanho da matriz
        max_node = max(max(edge) for edge in self.edges)
        self.len_mat = max_node

        # Inicialização das matrizes
        self.mat = np.zeros((self.len_mat + 1, self.len_mat + 1), dtype=int)
        self.apoio = np.zeros((self.len_mat + 1, self.len_mat + 1), dtype=int)
        self.final = np.zeros((self.len_mat + 1, self.len_mat + 1), dtype=int)

        # Preencher a matriz de adjacência
        for a, b in self.edges:
            self.mat[a][b] = 1
            self.final[a][b] = 1
            self.apoio[a][b] = 1

        # Verificar se camI e camJ estão dentro dos limites
        if self.camI > self.len_mat or self.camJ > self.len_mat or self.camI < 1 or self.camJ < 1:
            st.error("Os valores de partida e destino devem estar entre 1 e {}".format(self.len_mat))
            return

    def calcular_caminho(self):
        # Variável que controla se o caminho foi encontrado
        achou = True
        tamCaminho = 0

        # Calcula as potências da matriz de adjacência até encontrar um caminho
        for tamCaminho in range(1, self.len_mat):
            if self.mat[self.camI][self.camJ]:
                achou = False
                break

            # Multiplica as matrizes mat e apoio
            self.final = np.dot(self.mat, self.apoio)

            # Copia a matriz final para a matriz original
            self.mat = self.final.copy()

        # Exibir o resultado
        if achou:
            st.error("Não há caminho válido.")
        else:
            st.success(f"O menor número de caminhos de {self.camI} até {self.camJ} é: {tamCaminho}")

    def visualizar_grafo(self):
        # Visualizar o grafo
        G = nx.DiGraph()
        G.add_edges_from(self.edges)

        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G)  
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
        plt.title("Grafo")
        plt.axis('off') 

        # Exibir o grafo no Streamlit
        st.pyplot(plt)

    def executar(self):
        self.obter_entradas()
        self.processar_grafo()
        self.calcular_caminho()
        self.visualizar_grafo()
