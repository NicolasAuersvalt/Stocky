-- Apaga o banco se existir e cria um novo
DROP DATABASE IF EXISTS stockyutfpr;
CREATE DATABASE stockyutfpr;
USE stockyutfpr;

-- Tabela usuários (administradores e empresas)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    -- MODIFICADO: O ENUM agora aceita 'admin' e 'padrão' para alinhar com a aplicação.
    tipo ENUM('admin', 'padrão') NOT NULL
);

-- Tabela empresas (detalhes extras, vinculada a um usuário)
CREATE TABLE empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nome_fantasia VARCHAR(100),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela produtos, agora simplificada e vinculada diretamente à empresa
CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,      -- A qual empresa este produto pertence
    nome VARCHAR(255) NOT NULL,   -- Nome do produto
    categoria VARCHAR(100),       -- Categoria do produto
    preco DECIMAL(10,2) NOT NULL,
    quantidade INT NOT NULL DEFAULT 0, -- Adicionado para controle de estoque
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE
);

-- DADOS INICIAIS PARA TESTE

-- 1. Insere um administrador (terá id = 1)
-- MODIFICADO: Inserindo com o tipo 'admin'
INSERT INTO usuarios (nome, email, senha, tipo)
VALUES ('Admin Teste', 'admin@teste.com', SHA2('admin123', 256), 'admin');

-- 2. Insere um usuário para a empresa (terá id = 2)
-- MODIFICADO: Inserindo com o tipo 'padrão'
INSERT INTO usuarios (nome, email, senha, tipo)
VALUES ('Dono da Empresa', 'empresa@teste.com', SHA2('empresa123', 256), 'padrão');

-- 3. Cria o perfil da empresa, vinculando ao usuário de id = 2
INSERT INTO empresas (usuario_id, nome_fantasia)
VALUES (2, 'Empresa de Vinhos e Queijos LTDA');

-- 4. Insere produtos para a empresa de id = 1 (obtido do INSERT acima em 'empresas')
INSERT INTO produtos (empresa_id, nome, categoria, preco, quantidade)
VALUES 
(1, 'Vinho Tinto Seco', 'Bebidas', 50.00, 30),
(1, 'Vinho Branco Suave', 'Bebidas', 40.00, 25),
(1, 'Queijo Brie', 'Laticínios', 20.00, 50),
(1, 'Queijo Gorgonzola', 'Laticínios', 25.00, 40);