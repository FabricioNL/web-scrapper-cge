import sqlite3

# Função para criar o banco de dados e as tabelas
def create_database():
    conn = sqlite3.connect('dados_climaticos.db')
    c = conn.cursor()

    # Tabela Subprefeitura
    c.execute('''CREATE TABLE IF NOT EXISTS Subprefeitura (
                    id INTEGER PRIMARY KEY,
                    nome TEXT
                )''')

    # Tabela Chuvas
    c.execute('''CREATE TABLE IF NOT EXISTS Chuvas (
                    id INTEGER PRIMARY KEY,
                    subprefeitura_id INTEGER,
                    data TEXT,
                    quantidade_mm INTEGER,
                    FOREIGN KEY (subprefeitura_id) REFERENCES Subprefeitura(id)
                )''')

    # Tabela Alagamentos
    c.execute('''CREATE TABLE IF NOT EXISTS Alagamentos (
                    id INTEGER PRIMARY KEY,
                    subprefeitura_id INTEGER,
                    data TEXT,
                    quantidade_alagamentos INTEGER,
                    referencia TEXT,
                    sentido TEXT,
                    rua TEXT,
                    horario_inicio TEXT,
                    horario_fim TEXT,
                    FOREIGN KEY (subprefeitura_id) REFERENCES Subprefeitura(id)
                )''')

    conn.commit()
    conn.close()

# Função para inserir dados na tabela Subprefeitura
def insert_subprefeitura(nome_subprefeitura):
    conn = sqlite3.connect('dados_climaticos.db')
    c = conn.cursor()
    c.execute('''INSERT INTO Subprefeitura (nome) VALUES (?)''', (nome_subprefeitura,))
    conn.commit()
    conn.close()

# Função para inserir dados na tabela Chuvas
def insert_chuva(subprefeitura_id, data, quantidade_mm):
    conn = sqlite3.connect('dados_climaticos.db')
    c = conn.cursor()
    c.execute('''INSERT INTO Chuvas (subprefeitura_id, data, quantidade_mm) VALUES (?, ?, ?)''', (subprefeitura_id, data, quantidade_mm))
    conn.commit()
    conn.close()

# Função para inserir dados na tabela Alagamentos
def insert_alagamento(subprefeitura_id, data, quantidade_alagamentos, referencia, sentido, rua, horario_inicio, horario_fim):
    conn = sqlite3.connect('dados_climaticos.db')
    c = conn.cursor()
    c.execute('''INSERT INTO Alagamentos (subprefeitura_id, data, quantidade_alagamentos, referencia, sentido, rua, horario_inicio, horario_fim)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (subprefeitura_id, data, quantidade_alagamentos, referencia, sentido, rua, horario_inicio, horario_fim))
    conn.commit()
    conn.close()

# Criar o banco de dados e as tabelas
create_database()

