import requests
from bs4 import BeautifulSoup
import re
import sqlite3
from datetime import datetime, timedelta

# Função para criar uma lista de datas a partir de uma data inicial até uma data final
def create_dates(start, end):
    start_date = datetime.strptime(start, '%d/%m/%Y')
    end_date = datetime.strptime(end, '%d/%m/%Y')

    date_strings = []
    current_date = start_date
    while current_date <= end_date:
        date_strings.append(current_date.strftime('%d/%m/%Y'))
        current_date += timedelta(days=1)

    return date_strings

def split_from_last_number(text):
    match = re.search(r'(.+\d+:\d+)', text)
    if match:
        last_number_index = match.end()
        return text[:last_number_index], text[last_number_index:].strip()
    else:
        return text, ''


def split_from_reference(text):
    match = re.search(r'Referência:', text)
    if match:
        reference_index = match.start()
        return text[:reference_index], text[reference_index:]
    else:
        return text, ''

def insert_chuva(subprefeitura_id, data, quantidade_mm):
    conn = sqlite3.connect('dados_climaticos.db')
    c = conn.cursor()
    # Verifica se já existe uma entrada com os mesmos valores-chave
    c.execute('''SELECT COUNT(*) FROM Chuvas WHERE subprefeitura_id = ? AND data = ?''', (subprefeitura_id, data))
    if c.fetchone()[0] == 0:
        c.execute('''INSERT INTO Chuvas (subprefeitura_id, data, quantidade_mm) VALUES (?, ?, ?)''', (subprefeitura_id, data, quantidade_mm))
        conn.commit()
    conn.close()

def insert_alagamento(subprefeitura_nome, data, quantidade_alagamentos, referencia, sentido, rua, horario_inicio, horario_fim):
    conn = sqlite3.connect('backend/dados_climaticos.db')
    c = conn.cursor()
    # Verifica se a subprefeitura já existe na tabela Subprefeitura
    c.execute('''SELECT id FROM Subprefeitura WHERE nome = ?''', (subprefeitura_nome,))
    result = c.fetchone()
    # Se a subprefeitura não existe, insere-a na tabela Subprefeitura
    if not result:
        c.execute('''INSERT INTO Subprefeitura (nome) VALUES (?)''', (subprefeitura_nome,))
        subprefeitura_id = c.lastrowid
    else:
        subprefeitura_id = result[0]
        
    c.execute('''SELECT COUNT(*) FROM Alagamentos 
             WHERE subprefeitura_id = ? 
             AND data = ? 
             AND quantidade_alagamentos = ? 
             AND referencia = ? 
             AND sentido = ? 
             AND rua = ? 
             AND horario_inicio = ? 
             AND horario_fim = ?''', 
           (subprefeitura_id, data, quantidade_alagamentos, referencia, sentido, rua, horario_inicio, horario_fim))
    row_count = c.fetchone()[0]

    # Se não existe, inserir
    if row_count == 0:
        
        c.execute('''INSERT INTO Alagamentos (subprefeitura_id, data, quantidade_alagamentos, referencia, sentido, rua, horario_inicio, horario_fim)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (subprefeitura_id, data, quantidade_alagamentos, referencia, sentido, rua, horario_inicio, horario_fim))

        conn.commit()
        conn.close()
    else:
        conn.close()
        with open('log.txt', 'a') as log_file:
            log_file.write(f'Dados já inseridos para a subprefeitura {subprefeitura_nome}.\n')

yesterday = datetime.now() - timedelta(days=1)

dates_list = [yesterday.strftime('%d/%m/%Y')]

for start_date in dates_list:
    #escrita de log
    with open('log.txt', 'a') as log_file:
        log_file.write(f'Buscando dados para a data {start_date}.\n')
    
    print(f'Buscando dados para a data {start_date}.')
    
    dia = start_date.split('/')[0]
    mes = start_date.split('/')[1]
    ano = start_date.split('/')[2]

    url = f'https://www.cgesp.org/v3/alagamentos.jsp?dataBusca={dia}%2F{mes}%2F{ano}&enviaBusca=Buscar'
    response = requests.get(url)
    
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Se não houver registros para a data, passa para a próxima data
        if "Não há registros de alagamentos para essa data." in soup.text:
            print(f'Nao ha registros de alagamentos para a data {start_date}.')
            with open('log.txt', 'a') as log_file:
                log_file.write(f'Nao ha registros de alagamentos para a data {start_date}.\n')
                
            continue

        tables = soup.find_all('table', class_='tb-pontos-de-alagamentos')
        
        for table in tables:
        
            info = table.text
            info = info.split('\n')
            
            info = [x.replace('\r', '') for x in info]
            info = [x.replace('\t', '') for x in info]
            info = [x for x in info if x != '']
            
            regiao = info[0][:-1] #ok
            pontos = info[1].split(' ')[0] #ok
            
            #divide o restante da lista depois do segundo elemento em quantidade de pontos de alagamento
            for i in range(2, len(info), 2):
                horario, rua = split_from_last_number(info[i])
                horario_inicio = horario.split(' ')[1]
                horario_fim = horario.split(' ')[3] if len(horario.split(' ')) > 3 else ''
                sentido, referencia = split_from_reference(info[i+1])   
                sentido = sentido.split(' ')[1] if sentido else '' 
                referencia = referencia.split(' ')[1:] if referencia else ''
                
                if referencia != ' ':
                    referencia = ' '.join(referencia)
                
                # Inserindo dados de chuva e alagamento
                #insert_chuva(subprefeitura_id, start_date, pontos)
                insert_alagamento(regiao, start_date, pontos, referencia, sentido, rua, horario_inicio, horario_fim)
                with open('log.txt', 'a') as log_file:
                    log_file.write(f'Dados inseridos para a subprefeitura {regiao}.\n')
    else:
        print(f'Erro ao acessar a página. Código de status {response.status_code}.')
        with open('log.txt', 'a') as log_file:
            log_file.write(f'Erro ao acessar a página. Código de status {response.status_code}.\n')