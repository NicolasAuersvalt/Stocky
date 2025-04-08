from header import *

class Polinomio:
    def __init__(self, input_str):
        self.input = input_str.replace(' ', '')  # Remove espaços
        self.grau = 0
        self.v = []
        self.sinal = []
        self.r = []
        self.acha_grau()
        self.cria_vetor()
        pass

    def mod(self, x):
        return abs(x)

    def sinal_trocado(self, a, b):
        if b >= 0:
            return 0 if a >= 0 else 1
        else:
            return 1 if a >= 0 else 0

    def lim_pos(self):
        if self.grau % 2 and self.sinal[self.grau] == '-':
            return -1.0
        elif self.grau % 2 and self.sinal[self.grau] == '+':
            return +1.0
        elif self.sinal[self.grau] == '+':
            return +1
        else:
            return -1

    def lim_neg(self):
        if self.grau % 2 and self.sinal[self.grau] == '-':
            return +1.0
        elif self.grau % 2 and self.sinal[self.grau] == '+':
            return -1.0
        elif self.sinal[self.grau] == '+':
            return +1
        else:
            return -1

    def acha_grau(self):
        max_grau = 0
        for i in range(len(self.input)):
            if self.input[i] == 'x' and max_grau == 0:
                max_grau = 1
            if self.input[i] == '^':
                max_grau = max(max_grau, int(self.input[i + 1]))

        self.grau = max_grau
        self.v = [0] * (max_grau + 1)
        self.r = [0.0] * max_grau
        self.sinal = ['+'] * (max_grau + 1)

    def cria_vetor(self):
        inf = 0
        chave = 0
        while chave < len(self.input):
            if (self.input[chave] == '+' or self.input[chave] == '-') and chave > 0:
                self.exp = 0
                self.coe = 1
                sup = chave
                for i in range(inf, sup):
                    if self.input[i] == 'x':
                        self.exp = 1
                    if self.input[i] == '^':
                        self.exp = int(self.input[i + 1])
                    if self.input[i] == '*':
                        self.coe = int(self.input[i - 1])

                if self.input[inf] in ['+', '-']:
                    self.sinal[self.exp] = self.input[inf]
                    if self.exp == 0:
                        self.coe = int(self.input[inf + 1])
                else:
                    self.sinal[self.exp] = '+'
                    if self.exp == 0:
                        self.coe = int(self.input[inf])

                inf = sup
                self.v[self.exp] = self.coe

            chave += 1

        # Tratando o último termo após o loop
        if inf < chave:
            self.exp = 0
            self.coe = 1
            for i in range(inf, chave):
                if self.input[i] == 'x':
                    self.exp = 1
                if self.input[i] == '^':
                    self.exp = int(self.input[i + 1])
                if self.input[i] == '*':
                    self.coe = int(self.input[i - 1])

            if self.input[inf] in ['+', '-']:
                self.sinal[self.exp] = self.input[inf]
                if self.exp == 0:
                    self.coe = int(self.input[inf + 1])
            else:
                self.sinal[self.exp] = '+'
                if self.exp == 0:
                    self.coe = int(self.input[inf])

            self.v[self.exp] = self.coe

    def ex(self, base, expoente):
        return base ** expoente

    def valor(self, x):
        total = self.v[0] if self.sinal[0] == '+' else -self.v[0]
        for i in range(1, self.grau + 1):
            total += self.v[i] * self.ex(x, i) if self.sinal[i] == '+' else -self.v[i] * self.ex(x, i)
        return total
    
    def __str__(self):
        """Retorna a representação em string do polinômio."""
        partes = []
        for i in range(self.grau + 1):
            coef = self.v[i]
            if coef == 0:
                continue  # Ignora coeficientes zero
            sinal = self.sinal[i]
            parte = f"{'' if i == 0 else ('+' if sinal == '+' else '-')}{abs(coef)}"
            if i > 0:
                parte += f"*x"
            if i > 1:
                parte += f"^{i}"
            partes.append(parte)
        return ''.join(partes).replace('+-', '-').replace('x^1', 'x')  # Formatação adicional


    def derivada(self):
        d = Polinomio('')
        d.grau = self.grau - 1
        d.v = [0] * (d.grau + 1)
        d.sinal = ['+'] * (d.grau + 1)

        for i in range(d.grau + 1):
            d.v[i] = self.v[i + 1] * (i + 1)
            d.sinal[i] = self.sinal[i + 1]
        return d

    def primitiva(self, x):
        total = 0
        for i in range(self.grau + 1):
            total += (self.v[i] * self.ex(x, i + 1)) / (i + 1) if self.sinal[i] == '+' else -(self.v[i] * self.ex(x, i + 1)) / (i + 1)
        return total

    def area(self, a, b):
        return self.primitiva(b) - self.primitiva(a)

    def soma_Riemman(self, a, b, N):
        dx = (b - a) / N
        totalm = sum(self.valor(a + i * dx) * dx for i in range(N))
        totalM = sum(self.valor(a + (i + 1) * dx) * dx for i in range(N))
        total_medio = sum(self.valor(a + (i + 0.5) * dx) * dx for i in range(N))
        
        return totalm, totalM, total_medio

    def aprox(self, x):
        D = [1.0, 0.5, 0.1]
        der1 = self.derivada()
        der2 = der1.derivada()

        results = {}
        results["P(x)"] = self.valor(x)

        for d in D:
            linear = self.valor(x - d) + der1.valor(x - d) * d
            quadratica = (self.valor(x - d) +
                          der1.valor(x - d) * d +
                          der2.valor(x - d) * d**2 / 2)
            results[f'Aproximação linear com d={d}'] = linear
            results[f'Aproximação quadrática com d={d}'] = quadratica
        
        return results