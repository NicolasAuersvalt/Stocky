from header import *
from src.grafica import *
import json
import os

text_path = os.path.join('assets', 'textos', 'grafica.json')
imagem_path = "assets/coordenada.PNG"  # Substitua pelo caminho da sua imagem

# Carregar os dados do arquivo JSON
with open(text_path, 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Função para as operações
def pagina_operacoes():
    st.title("Operações com Matrizes com Visualização 3D")

    # Menu lateral para escolher a operação
    opcao = st.sidebar.selectbox("Escolha a operação", ("Teoria", "Ampliação", "Translação", "Rotação"))

    # Entrada de texto para a matriz inicial
    matriz_str = st.text_area("Matriz do CUBO (use notação Python, ex: [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])", 
                              "[[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]")

    # Converter a string de entrada para lista
    try:
        matriz = np.array(eval(matriz_str))
    except Exception as e:
        st.error("Erro ao converter a matriz. Verifique a entrada.")

    transformacao = Transformacao3D(matriz)

    # Verificar se a matriz é 3xn
    if matriz.ndim != 2 or matriz.shape[1] != 3:
        st.error("A matriz deve ter 3 colunas.")
    else:
        
        resultado = None
        
        if opcao == "Teoria":
            resultado = teoria()

        if opcao == "Ampliação":
            resultado = transformacao.ampliar()

        elif opcao == "Translação":
            resultado = transformacao.transladar()

        elif opcao == "Rotação":
            resultado = transformacao.rotacionar()

        if resultado is not None:

            # Plotar o gráfico 3D do resultado
            st.plotly_chart(transformacao.plot_matriz_3d(resultado))

            # Exibir o resultado
            st.write("Resultado:")
            st.write(resultado)

def teoria():
    st.subheader("Computação Gráfica")
    st.write("""
        Este aplicativo é uma aplicação da Álgebra Linear na computação gráfica.
    """)
    st.write(dados['Grafica'])
    st.image(imagem_path, caption="Conversão para Polar", width=400)
    st.write(dados['Grafica2'])