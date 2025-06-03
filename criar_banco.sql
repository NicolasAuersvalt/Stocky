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
    tipo ENUM('administrador', 'empresa') NOT NULL
);

-- Tabela empresas (detalhes extras para empresa, vinculada a usuarios tipo 'empresa')
CREATE TABLE empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nome_fantasia VARCHAR(100),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela estoque, vinculada à empresa
CREATE TABLE estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE
);

-- Tabela produtos, vinculada ao estoque
CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estoque_id INT NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (estoque_id) REFERENCES estoque(id) ON DELETE CASCADE
);

-- Dados iniciais para teste

-- Insere um administrador
INSERT INTO usuarios (nome, email, senha, tipo)
VALUES ('Admin Teste', 'admin@teste.com', SHA2('admin123', 256), 'administrador');

-- Insere uma empresa vinculada a um usuário do tipo empresa
INSERT INTO usuarios (nome, email, senha, tipo)
VALUES ('Empresa Teste', 'empresa@teste.com', SHA2('empresa123', 256), 'empresa');

INSERT INTO empresas (usuario_id, nome_fantasia)
VALUES (2, 'Empresa Teste LTDA');

-- Insere um estoque vinculado à empresa
INSERT INTO estoque (empresa_id, tipo)
VALUES (1, 'Bebidas'), (1, 'Queijos');

-- Insere produtos vinculados aos estoques
INSERT INTO produtos (estoque_id, tipo, preco)
VALUES 
(1, 'Vinho Tinto', 50.00),
(1, 'Vinho Branco', 40.00),
(2, 'Queijo Brie', 20.00);
