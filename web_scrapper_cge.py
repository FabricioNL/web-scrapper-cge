from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import pandas as pd
from datetime import datetime, timedelta

#cria uma lista de strings em que cada string é uma data a partir de uma string de data até uma string de data
def create_dates(start, end):
    # Converter as strings de data para objetos datetime
    start_date = datetime.strptime(start, '%d/%m/%Y')
    end_date = datetime.strptime(end, '%d/%m/%Y')

    # Lista para armazenar as datas como strings
    date_strings = []

    # Iterar sobre o intervalo de datas e adicionar cada uma à lista
    current_date = start_date
    while current_date <= end_date:
        date_strings.append(current_date.strftime('%d/%m/%Y'))
        current_date += timedelta(days=1)

    return date_strings

start_date = '05/03/2024'
end_date = '05/03/2024'
dates_list = create_dates(start_date, end_date)
grupos = []

with webdriver.Firefox() as driver:

    driver.get("https://www.cgesp.org/v3/alagamentos.jsp")
    wait = WebDriverWait(driver, 10)
    
    #procura o elemento de input da data inicial
    date_input = driver.find_element(By.XPATH, '//*[@id="campoBusca"]')
    date_input.clear()
    date_input.send_keys(start_date)
    
    #pressiona o botao de busca
    date_input.send_keys(Keys.RETURN)
    
    time.sleep(3)
    
    #se encontrar "Não há registros de alagamentos para essa data." então pula para a próxima data
    if driver.find_elements(By.CLASS_NAME, 'content'):
        if driver.find_element(By.CLASS_NAME, 'content').text == "Não há registros de alagamentos para essa data.":
            print("Não há registros de alagamentos para essa data.")
        else:
            for table in driver.find_elements(By.CLASS_NAME, 'tb-pontos-de-alagamentos'):
                #transforma a tabela em texto 
                infos = table.text
                infos = infos.split('\n')
    
                print(infos)
                
                regiao = infos[0]
                pontos = infos[1].split(' ')[0]
    
                for i in range(2, len(infos), 4):
                # Extrair um grupo de 4 elementos
                    grupo = infos[i:i+4]
                    grupo.append(regiao)
                    grupo.append(pontos)
                    grupo.append(start_date)
                    grupos.append(grupo)
                    print(grupos)
                    
    print(grupos)
    df = pd.DataFrame(grupos, columns=['Horario', 'Rua', 'Sentido', 'Referência', "Região", "Pontos", "Data"])
    df.to_excel('ALAGAMENTOS_CGE.xlsx', index=False)

        
    
    
    
    
    
    
    
    
