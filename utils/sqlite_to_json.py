import sqlite3
import json

# Conecte ao banco de dados SQLite
conn = sqlite3.connect('dados_climaticos.db')
cursor = conn.cursor()

# Obtenha todos os dados de uma tabela
cursor.execute("SELECT * FROM Alagamentos")
rows = cursor.fetchall()

# Obtenha os nomes das colunas
columns = [desc[0] for desc in cursor.description]

# Converta os dados para JSON
data = [dict(zip(columns, row)) for row in rows]

# Salve em um arquivo JSON
with open('alagamentos.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Exportação para JSON concluída!")
