import requests
from bs4 import BeautifulSoup
import re
import sqlite3
from datetime import datetime, timedelta
import pytz


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
    c.execute('''INSERT INTO Chuvas (subprefeitura_id, data, quantidade_mm) VALUES (?, ?, ?)''', (subprefeitura_id, data, quantidade_mm))
    conn.commit()
    conn.close()

def insert_alagamento(subprefeitura_id, data, quantidade_alagamentos, referencia, sentido, rua, horario_inicio, horario_fim):
    conn = sqlite3.connect('dados_climaticos.db')
    c = conn.cursor()
    c.execute('''INSERT INTO Alagamentos (subprefeitura_id, data, quantidade_alagamentos, referencia, sentido, rua, horario_inicio, horario_fim)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (subprefeitura_id, data, quantidade_alagamentos, referencia, sentido, rua, horario_inicio, horario_fim))
    conn.commit()
    conn.close()

brt = pytz.timezone('America/Sao_Paulo')

yesterday_brt = datetime.now(brt) - timedelta(days=1)
end_date = yesterday_brt.strftime('%d/%m/%Y')

dates_list = [end_date]

for start_date in dates_list:
    dia = start_date.split('/')[0]
    mes = start_date.split('/')[1]
    ano = start_date.split('/')[2]

    url = f'https://www.cgesp.org/v3/alagamentos.jsp?dataBusca={dia}%2F{mes}%2F{ano}&enviaBusca=Buscar'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Se não houver registros para a data, passa para a próxima data
        if "Não há registros de alagamentos para essa data." in soup.text:
            print(f'Não há registros de alagamentos para a data {start_date}.')
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
                horario_fim = horario.split(' ')[3]
                sentido, referencia = split_from_reference(info[i+1])    
                
                # Obtendo ou inserindo a subprefeitura e obtendo seu ID
                conn = sqlite3.connect('dados_climaticos.db')
                c = conn.cursor()
                c.execute('''SELECT id FROM Subprefeitura WHERE nome = ?''', (regiao,))
                result = c.fetchone()
                if result:
                    subprefeitura_id = result[0]
                else:
                    c.execute('''INSERT INTO Subprefeitura (nome) VALUES (?)''', (regiao,))
                    subprefeitura_id = c.lastrowid
                conn.close()
                
                # Inserindo dados de chuva e alagamento
                insert_chuva(subprefeitura_id, start_date, pontos)
                insert_alagamento(subprefeitura_id, start_date, pontos, referencia, sentido, rua, horario_inicio, horario_fim)
