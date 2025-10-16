"""Asignatura: SGDI

Práctica 1: Web Scraping

Autores:
- MARIA JOSÉ GRIMALDI FERNÁNDEZ
- NATALIA PALOMA LA ROSA MONTERO
- IREMAR LUHETSY RIVAS ÁLVAREZ

Declaración de integridad
Declaramos que esta solución es fruto exclusivamente de nuestro trabajo
personal. No hemos sido ayudados por ninguna otra persona o sistema automático
ni hemos obtenido la solución de fuentes externas, y tampoco hemos compartido
nuestra solución con otras personas de manera directa o indirexcta.
Declaramos además que no hemos realizado de manera deshonesta ninguna otra
actividad que pueda mejorar nuestros resultados ni perjudicar los resultados
de los demás.
"""

import requests
from bs4 import BeautifulSoup
def bd_incrementos(umbral):
     
    r = requests.get('https://db-engines.com/en/ranking', auth=('user', 'pass'))
    r.status_code

    soup = BeautifulSoup(r.text, 'html5lib')
    tabla_necesaria = soup.find_all("table", "dbi")
    tabla_necesaria_primer_elemento = tabla_necesaria[0]
    tabla_tbody = tabla_necesaria_primer_elemento.tbody
    tabla_tr = tabla_tbody.find_all("tr")

    tabla_tr_partida = tabla_tr[3:]

    fragmentos = []

    for row in tabla_tr_partida:    
        tabla_enlaces = row.find_all("a")
        
        NOMBRE_BD = tabla_enlaces[0].find(string=True, recursive=False)
        
        if(len(tabla_enlaces) > 1):
            MODELO_PRINCIPAL_BD = tabla_enlaces[1].find(string=True, recursive=False).strip()
        else:
            tabla_th = row.find_all('th')
            texto = tabla_th[1].find(string=True, recursive=False)
            MODELO_PRINCIPAL_BD = texto.strip()
        
        tabla_td = row.find_all("td")
        ultima_columna = tabla_td[-1]
        tabla_ultima_columna = ultima_columna.contents
        if(tabla_ultima_columna):
            INCREMENTO_PUNTUACIÓN_ANUAL = tabla_ultima_columna[0]
            if(type(INCREMENTO_PUNTUACIÓN_ANUAL) != float):
                INCREMENTO_PUNTUACIÓN_ANUAL = float(INCREMENTO_PUNTUACIÓN_ANUAL.replace('±', ''))
        else:
            INCREMENTO_PUNTUACIÓN_ANUAL = 0.00
                        
        fragmentos.append((NOMBRE_BD, MODELO_PRINCIPAL_BD, INCREMENTO_PUNTUACIÓN_ANUAL))
    ordenados = sorted(fragmentos, key=lambda x: x[2], reverse=True)    
    mayores = list(filter(lambda x: x[2] > umbral, ordenados))

    print("[")
    for mayor in mayores:
        print(f" {mayor},")
    print("]")


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
def citas_celebres(autor):
    
    driver = webdriver.Chrome()
    driver.get("https://quotes.toscrape.com/search.aspx")

    driver.implicitly_wait(20)

    element_author = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "author")))
    element_author.click()
    element_author.send_keys(autor)
    element_author.click()

    html_for_tags = driver.page_source

    html_quotes = []
    
    soup_for_tags = BeautifulSoup(html_for_tags, 'html5lib')
    select_tag = soup_for_tags.css.select('select#tag')
    options = select_tag[0].find_all("option")

    quotes_by_tag = {}

    for option in options[1:]:
        driver.implicitly_wait(20)
        
        tag = option.getText().strip()

        element_tag = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "tag")))

        element_tag.click()
        element_tag.send_keys(tag)
        
        element_tag.click()

        element_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "submit_button")))

        element_button.click()

        driver.implicitly_wait(20)
 
        WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "quote")))

        WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "content")))
 
        html_quotes.append([tag, driver.page_source]) 

    for tag, html_quote in html_quotes:
        soup_quote = BeautifulSoup(html_quote, 'html5lib')
        results = soup_quote.find("div", class_="results")
        quotes = results.find_all("div", class_="quote")

        
        for quote in quotes:
            content = quote.find("span", class_="content")

            if tag not in quotes_by_tag:
                quotes_by_tag[tag] = []

            quotes_by_tag[tag].append(f"{content.getText().strip()}")
 
    for tag, quotes in quotes_by_tag.items():
        print(f"'{tag}': {quotes}\n")


def tags_por_autor():
    driver = webdriver.Chrome()
    driver.get("https://quotes.toscrape.com/search.aspx")
    driver.implicitly_wait(20)

    html_autor = driver.page_source
    soup_autor = BeautifulSoup(html_autor, 'html5lib')
    select_author = soup_autor.css.select('select#author')
    options_authors = select_author[0].find_all("option")

    tags_per_author = {}

    for option_author in options_authors[1:]:
        author = option_author.getText().strip()
        
        element_author = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "author")))
        
        element_author.click()
        element_author.send_keys(author)
        
        element_author = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "author")))
        
        element_author.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "tag")))

        html_tag = driver.page_source
        soup_tag = BeautifulSoup(html_tag, 'html5lib')
        select_tag = soup_tag.css.select('select#tag')
        options_tags = select_tag[0].find_all("option")

        numero_tags = len(options_tags[1:])

        if author not in tags_per_author:
            tags_per_author[author] = []

        tags_per_author[author] = numero_tags

    driver.close()

    print(tags_per_author)

#bd_incrementos(2)
#citas_celebres("Jane Austen")
tags_por_autor()