import sqlite3

# Conectar ao banco de dados (será criado se não existir)
conn = sqlite3.connect('usuarios.db')
c = conn.cursor()

# Criar tabela de usuários
c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    )
''')

# Inserir usuário administrador padrão, se não existir
c.execute('SELECT * FROM usuarios WHERE username = "nicolas"')
if not c.fetchone():
    c.execute('INSERT INTO usuarios (username, password, is_admin) VALUES (?, ?, ?)', ('nicolas', '123', 1))

conn.commit()
conn.close()

