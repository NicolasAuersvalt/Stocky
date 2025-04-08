# Usar a imagem base do Python
FROM python:3.12-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requirements e o código da aplicação para o contêiner
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos da aplicação
COPY . .

# Expor a porta em que o Streamlit irá rodar
EXPOSE 8501

# Comando para iniciar a aplicação Streamlit
CMD ["streamlit", "run", "App.py", "--server.port=8501", "--server.address=0.0.0.0"]
