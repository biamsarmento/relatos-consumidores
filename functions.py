from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import csv

def go_to_work(data_inicio, data_fim):
    # Dividir as datas em intervalos de uma semana
    semanas = week_division(data_inicio, data_fim)

    # Loop para filtrar e salvar os dados de cada semana
    for semana in semanas:
        get_data(semana)


def week_division(data_inicio, data_fim):
    data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
    data_fim = datetime.strptime(data_fim, "%d/%m/%Y")
    intervalos = []
    while data_inicio <= data_fim:
        semana_fim = data_inicio + timedelta(days=6)
        if semana_fim > data_fim:
            semana_fim = data_fim
        intervalos.append((data_inicio, semana_fim))
        data_inicio = semana_fim + timedelta(days=1)
    return intervalos

def filter(data_termino, driver):

    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-toggle='dropdown']"))).click()
    except TimeoutException:
        print("Dropdown não encontrado")
        return False

    try: 
    # Aguarde até que o pop-up seja exibido
        popup = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "menu-suspenso")))
    except TimeoutException:
        print("Menu-Suspenso não encontrado")
        return False

    data_termino_dia_seguinte = (datetime.strptime(data_termino, "%d/%m/%Y") + timedelta(days=1)).strftime("%d/%m/%Y")

    try:
        data_termino_input = popup.find_element(By.ID, "dataTermino")
        data_termino_input.click()
        data_termino_input.clear()
        data_termino_input.send_keys(data_termino_dia_seguinte)
    except NoSuchElementException:
        print("Elemento não encontrado. O input 'dataTermino' NÃO está presente no pop-up.")
        return False

    # Localiza o elemento do botão "Pesquisar" e clique nele
    try:
        pesquisar_button = popup.find_element(By.ID, "btn-pesquisar")
        pesquisar_button.click()
    except NoSuchElementException:
        print("Botão 'Pesquisar' não encontrado.")
        return False

    try:
        WebDriverWait(driver, 300).until(EC.invisibility_of_element_located((By.ID, "btn-pesquisar")))
    except TimeoutException:
        print("O resultado da pesquisa demorou mais de 240s!")
        return False
    
    return True

def click_button(data_inicio, driver):
    # Numero de paginas
    pag = 0
    datas_cartoes = []
    continua = True

    while continua:  
        html = driver.page_source
        new_soup = BeautifulSoup(html, 'lxml')
        resultados = new_soup.find('div', {"id": "resultados"})
        cartoes = resultados.find_all('div', class_="cartao-relato")
        
        for cartao in cartoes:
            data = cartao.find('span', class_="relatos-data").text.strip().split(',')
            datas_cartoes.append(data)

        # Encontre a data mais recente
        if datas_cartoes:
            ultima_data_str = datas_cartoes[-1][0].strip()  # Última data como string
            ultima_data = datetime.strptime(ultima_data_str, "%d/%m/%Y")  # Converta para um objeto de data

            # Verifique se a data do último cartão é maior ou igual à data de início
            if ultima_data >= datetime.strptime(data_inicio, "%d/%m/%Y"):
                
                # Verifique se o botão "Mais Resultados" está disponível
                try:
                    mais_resultados_button = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.ID, "btn-mais-resultados")))
                    mais_resultados_button.click()
                    datas_cartoes = []
                    
                    # Obtenha a data do último cartão após clicar no botão
                    html = driver.page_source
                    new_soup = BeautifulSoup(html, 'lxml')
                    resultados = new_soup.find('div', {"id": "resultados"})
                    cartoes = resultados.find_all('div', class_="cartao-relato")
                    ultima_data_str = cartoes[-1].find('span', class_="relatos-data").text.strip().split(',')[0].strip()
                    ultima_data = datetime.strptime(ultima_data_str, "%d/%m/%Y")           
                except TimeoutException:
                    print("Botão 'Mais Resultados' não disponível após 240s.")
                    continua = False
                    return False
            else:
                continua = False

        # Obter os cartões novamente após clicar no botão
        html = driver.page_source
        new_soup = BeautifulSoup(html, 'lxml')
        resultados = new_soup.find('div', {"id": "resultados"})
        cartoes = resultados.find_all('div', class_="cartao-relato")

    return True

# Função principal para realizar a filtragem e salvar os dados
def get_data(intervalo):
    data_inicio_str = intervalo[0].strftime("%d/%m/%Y")
    data_fim_str = intervalo[1].strftime("%d/%m/%Y")
    todos_os_catoes_carregaram = False
    filtro_carregou = False

    driver = webdriver.Chrome()
    url = 'https://www.consumidor.gov.br/pages/indicador/relatos/abrir'
    driver.get(url)
    
    filtro_carregou = filter(data_fim_str, driver)

    if filtro_carregou:

        todos_os_catoes_carregaram = click_button(data_inicio_str, driver)

        if todos_os_catoes_carregaram:
            html = driver.page_source
            new_soup = BeautifulSoup(html, 'lxml')
            resultados = new_soup.find('div', {"id": "resultados"})
            cartoes = resultados.find_all('div', class_="cartao-relato")

            # Salvar os dados em um CSV
            data_inicio_str_safe = data_inicio_str.replace("/", "-")
            data_fim_str_safe = data_fim_str.replace("/", "-")
            nome_arquivo = f'dados_{data_inicio_str_safe}_a_{data_fim_str_safe}.csv'
            
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Empresa', 'Data', 'Local', 'Status', 'Relato', 'Resposta', 'Nota', 'Comentario']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for cartao in cartoes:

                    data_local = cartao.find('span', class_="relatos-data").text.strip()
                    data, local = data_local.split(',', 1)  # Divide em duas partes, apenas uma vez

                    # Convertendo a data para o formato datetime
                    data_cartao = datetime.strptime(data.strip(), "%d/%m/%Y").date()
                
                    # Verifica se a data do cartão está dentro do intervalo especificado
                    if (data_cartao >= datetime.strptime(data_inicio_str, "%d/%m/%Y").date()) and (data_cartao <= datetime.strptime(data_fim_str, "%d/%m/%Y").date()):

                        empresa = cartao.find('a').text
                        
                        status = cartao.find('h4').text.strip()

                        strong_tags = cartao.find_all('strong')
                        relato_found = False
                        resposta_found = False
                        for strong_tag in strong_tags:
                            if strong_tag.text.strip() == 'Relato':
                                relato_found = True
                                # Encontra todos os paragrafos apos a tag <strong>Relato</strong>
                                paragrafos_relato = []
                                next_sibling = strong_tag.find_next_sibling()
                                while next_sibling and next_sibling.name != 'strong':
                                    if next_sibling.name == 'p':
                                        paragrafos_relato.append(next_sibling.text.strip())
                                    next_sibling = next_sibling.find_next_sibling()

                        if relato_found:
                            # Procura a tag <strong>Resposta</strong>
                            for strong_tag in strong_tags:
                                if strong_tag.text.strip() == 'Resposta':
                                    resposta_found = True
                                    # Encontrar todos os parágrafos após a tag <strong>Resposta</strong>
                                    paragrafos_resposta = []
                                    next_sibling = strong_tag.find_next_sibling()
                                    while next_sibling and next_sibling.name != 'strong':
                                        if next_sibling.name == 'p':
                                            paragrafos_resposta.append(next_sibling.text.strip())
                                        next_sibling = next_sibling.find_next_sibling()

                        if resposta_found:
                            # Procura a tag <strong>Resposta</strong>
                            for strong_tag in strong_tags:
                                if strong_tag.text.strip() == 'Avaliação':
                                    # Encontrar todos os parágrafos após a tag <strong>Resposta</strong>
                                    paragrafos_avaliacao = []
                                    next_sibling = strong_tag.find_next_sibling()
                                    while next_sibling and next_sibling.name != 'strong':
                                        if next_sibling.name == 'p':
                                            paragrafos_avaliacao.append(next_sibling.text.strip())
                                        next_sibling = next_sibling.find_next_sibling()

                                    if paragrafos_avaliacao:

                                        for paragrafo in paragrafos_avaliacao:
                                            if paragrafo.startswith('Nota '):
                                                nota = paragrafo.replace('Nota ', '').strip()
                                            else:                                 
                                                comentario = paragrafo.strip()

                                        # Escrever os dados no CSV
                                        writer.writerow({'Empresa': empresa, 'Data': data, 'Local': local.strip(), 'Status': status, 'Relato': '\n'.join(paragrafos_relato).strip(), 'Resposta': '\n'.join(paragrafos_resposta).strip(), 'Nota': nota, 'Comentario': comentario})

                                        break
        else:
            print("Os cartões não foram todos abertos!")
    else:
        print("Filtro não carregou!")

    driver.quit()

