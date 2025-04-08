import numpy as np
import plotly.graph_objects as go
import streamlit as st

class Transformacao3D:
    def __init__(self, matriz):
        self.matriz = matriz


    def plot_matriz_3d(self, matriz):
        arestas = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # Base
            [4, 5], [5, 6], [6, 7], [7, 4],  # Topo
            [0, 4], [1, 5], [2, 6], [3, 7]   # Conexões
        ]
        
        x = matriz[:, 0]
        y = matriz[:, 1]
        z = matriz[:, 2]

        fig = go.Figure()

        for aresta in arestas:
            fig.add_trace(go.Scatter3d(
                x=[x[aresta[0]], x[aresta[1]]],
                y=[y[aresta[0]], y[aresta[1]]],
                z=[z[aresta[0]], z[aresta[1]]],
                mode='lines',
                line=dict(color='blue', width=5)
            ))

        # Definir os limites dos eixos manualmente para 10x10x10
        fig.update_layout(title="Visualização 3D do Cubo", autosize=True,
                        scene=dict(
                            xaxis=dict(range=[-3, 3]),
                            yaxis=dict(range=[-3, 3]),
                            zaxis=dict(range=[-3, 3])
                        ),
                        margin=dict(l=65, r=50, b=65, t=90))
        return fig

    def rotacionar(self):
        angulo_x = st.slider("Ângulo de Rotação de X (graus)", min_value=0, max_value=360, value=45)
        angulo_y = st.slider("Ângulo de Rotação de Y (graus)", min_value=0, max_value=360, value=45)
        angulo_z = st.slider("Ângulo de Rotação de Z (graus)", min_value=0, max_value=360, value=45)

        angulo_radX = np.radians(angulo_x)
        angulo_radY = np.radians(angulo_y)
        angulo_radZ = np.radians(angulo_z)

        matriz_rotacaoX = np.array([[1, 0, 0],
                                    [0, np.cos(angulo_radX), -np.sin(angulo_radX)],
                                    [0, np.sin(angulo_radX), np.cos(angulo_radX)]])
        
        matriz_rotacaoY = np.array([[np.cos(angulo_radY), 0, np.sin(angulo_radY)],
                                    [0, 1, 0],
                                    [-np.sin(angulo_radY), 0, np.cos(angulo_radY)]])
        
        matriz_rotacaoZ = np.array([[np.cos(angulo_radZ), -np.sin(angulo_radZ), 0],
                                    [np.sin(angulo_radZ), np.cos(angulo_radZ), 0],
                                    [0, 0, 1]])

        # R = R1 * R2 * R3 => R = R1 * (R2*R3) => R = R1 * Rr, Rr = (R2*R3)
        matriz_Rr = self.multiplicar_matrizes(matriz_rotacaoZ, matriz_rotacaoY)
        matriz_R = self.multiplicar_matrizes(matriz_rotacaoX, matriz_Rr)

        # Aplicar a matriz de rotação à matriz original (P' = R * P)
        resultado = self.multiplicar_matrizes(matriz_R, self.matriz.T).T

        return resultado

    def ampliar(self):
        coef = st.number_input("Coeficiente de Ampliação:", value=1.0, min_value=0.0)

        # Multiplicando a matriz pelos coeficientes de ampliação
        resultado = self.matriz * coef

        return resultado

    def transladar(self):
        # Sliders para descolamento
        deslocamento_x = st.slider("Deslocamento X", min_value=-10.0, max_value=10.0, value=0.0)
        deslocamento_y = st.slider("Deslocamento Y", min_value=-10.0, max_value=10.0, value=0.0)
        deslocamento_z = st.slider("Deslocamento Z", min_value=-10.0, max_value=10.0, value=0.0)

        # Criar a matriz de deslocamento
        matriz_deslocamento = np.array([
            [deslocamento_x] * self.matriz.shape[0],
            [deslocamento_y] * self.matriz.shape[0],
            [deslocamento_z] * self.matriz.shape[0]
        ]).T

        # Somar as matrizes
        resultado = self.matriz + matriz_deslocamento

        return resultado

    def multiplicar_matrizes(self, matriz1, matriz2):
        return np.dot(matriz1, matriz2)

    def somar_matrizes(self, matriz1, matriz2):
        return np.add(matriz1, matriz2)

    def executar(self):
        # Exemplo de uso das funções da classe
        self.matriz = self.rotacionar()
        self.matriz = self.ampliar()
        self.matriz = self.transladar()
        fig = self.plot_matriz_3d()
        st.plotly_chart(fig)

