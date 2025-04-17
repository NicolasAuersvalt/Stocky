# Stocky

![Stocky](assets/logo_texto.png)

---

Federal University of Technology - Paraná (2025)

---


Developed by:

Felipe da Silva Mossato

Larissa Behrens Soares

Nícolas Auersvalt Marques

Nicolas Rossi Gariba

---

https://stockyapp.streamlit.app/

## Requisitos Mínimos

Antes de executar o site, certifique-se de ter as seguintes ferramentas instaladas no seu sistema:

python 3.8

streamlit

## Instalação

Para desenvolver, use:

    mkdir Stocky && cd Stocky
    git clone https://github.com/NicolasAuersvalt/Stocky.git
    cd Stocky

Para instalar as dependências, execute o script `instalador.sh`:

    chmod +x instalador.sh
    ./instalador.sh

---

## Execução

Após a instalação, para rodar o site localmente, utilize:

    streamlit run app.py
    
---

O Stocky é uma plataforma de controle de estoque pensada para empresas que têm vários vendedores. Cada vendedor só enxerga os produtos aos quais tem autorização e pode registrar entradas (compras, ajustando o saldo e informando o custo) e saídas (vendas, reduzindo o estoque e definindo o preço de venda). Do outro lado, o administrador vê tudo: o catálogo completo da empresa e os estoques individuais de cada vendedor, com detalhes de quantidade, custos de compra e valores de venda ao longo do tempo.

Desenvolvido em Python com Streamlit e MySQL, o Stocky adota boas práticas de segurança: as credenciais ficam protegidas em variáveis de ambiente , e cada usuário autentica-se com login e senha próprios antes de acessar sua área. Dessa forma, mantemos seus dados seguros e seu controle de estoque sempre confiável.