from header import *
from src.polinomio import *

def pagina_polinomios():
    st.title("Calculadora de Polinômios")

    opcoes = st.sidebar.selectbox("Escolha uma operação:", ["Teoria", "Polinomios"])

    if opcoes == "Teoria":
        teoria()
    elif opcoes == "Polinomios":
        pol()

def teoria():
    st.write("Teoria Usada em Polinomios..............")

def pol():
    entrada = st.text_input("Digite o polinômio (exemplo: 2*x^2 - 3*x + 5):")
    
    if entrada:
        polinomio = Polinomio(entrada)
        
        # Geração do gráfico
        x_values = np.linspace(-10, 10, 400)  # Gera 400 pontos de -10 a 10
        y_values = [polinomio.valor(x) for x in x_values]  # Avalia o polinômio em cada ponto

        plt.figure(figsize=(10, 5))
        plt.plot(x_values, y_values, label=f'P(x) = {polinomio}', color='blue')
        plt.title("Gráfico do Polinômio")
        plt.xlabel("x")
        plt.ylabel("P(x)")
        plt.axhline(0, color='black', lw=0.5, ls='--')
        plt.axvline(0, color='black', lw=0.5, ls='--')
        plt.grid()
        plt.legend()
        
        opcoes = st.selectbox("Escolha uma operação:", ["Derivada", "Primitiva", "Soma de Riemann", "Aproximação"])
        
        if opcoes == "Derivada":
            resultado = polinomio.derivada()
            st.write(f"A derivada do polinômio é: {resultado}")
        
        elif opcoes == "Primitiva":
            x = st.number_input("Digite o ponto para calcular a primitiva:", value=0.0)
            resultado = polinomio.primitiva(x)
            st.write(f"A primitiva do polinômio em x={x} é: {resultado}")
        
        elif opcoes == "Soma de Riemann":
            a = st.number_input("Digite o limite inferior:", value=0.0)
            b = st.number_input("Digite o limite superior:", value=1.0)
            n = st.number_input("Digite o número de subintervalos:", value=10)
            resultado_totalm, resultado_totalM, resultado_total_medio = polinomio.soma_Riemman(a, b, n)
            st.write(f"A soma de Riemann (mínima) é: {resultado_totalm}")
            st.write(f"A soma de Riemann (máxima) é: {resultado_totalM}")
            st.write(f"A soma de Riemann (média) é: {resultado_total_medio}")
        
        elif opcoes == "Aproximação":
            x = st.number_input("Digite o ponto de aproximação:", value=0.0)
            resultado = polinomio.aprox(x)
            st.write(f"A aproximação em x={x} é:")
            for key, value in resultado.items():
                st.write(f"- {key}: {value}")
                
        st.pyplot(plt)