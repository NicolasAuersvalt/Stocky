import streamlit as st
import numpy as np

class Cifra:
    def __init__(self):
        self.grau = None
        self.matriz = None
        self.senha = None
        self.senha_sem_espacos = None

    def receber_entradas(self):
        # Receber o grau
        self.grau = st.number_input("Digite o Grau:", min_value=1, step=1)

        # Receber a matriz de transformação (CHAVE) como texto
        matriz_input = st.text_area("Digite a Matriz Codificadora (linha por linha, separados por espaços):")

        # Processar a entrada da matriz
        if matriz_input:
            matT = []
            linhas = matriz_input.strip().split('\n')
            for linha in linhas:
                matT.append(list(map(int, linha.split())))

            matT = np.array(matT)

            if matT.shape != (self.grau, self.grau):
                st.error(f"A matriz deve ser de dimensão {self.grau}x{self.grau}.")
                return False
            self.matriz = matT

            # Receber a senha
            self.senha = st.text_area("Digite a String (letras e espaços serão removidos):")

            # Remover espaços da string
            self.senha_sem_espacos = ''.join(c for c in self.senha.upper() if c.isalpha())
            return True
        return False

    def cifrar(self):
        # Analisar o Resto
        tamSenha = len(self.senha_sem_espacos)
        resto = tamSenha % self.grau

        # Se não for divisível, preenche com o último caractere
        if resto != 0:
            ultimo = self.senha_sem_espacos[-1]
            self.senha_sem_espacos += ultimo * (self.grau - resto)

        criptografado = []

        # Percorrer todos os agrupamentos
        for i in range(0, len(self.senha_sem_espacos), self.grau):
            agrupamento = [(ord(self.senha_sem_espacos[i + j]) - ord('A') + 1) for j in range(self.grau)]

            # Produto da matriz com vetor agrupamento
            for m in range(self.grau):
                produto = sum(self.matriz[m][n] * agrupamento[n] for n in range(self.grau))
                produto = produto % 26 
                if produto == 0: produto = 26 
                criptografado.append(produto) 

        # Exibir o resultado criptografado
        st.subheader("Resultado Criptografado:")
        resultado = ''.join(chr(c + ord('A') - 1) for c in criptografado)
        st.write(resultado)

    def executar(self):
        if self.receber_entradas():
            self.cifrar()
