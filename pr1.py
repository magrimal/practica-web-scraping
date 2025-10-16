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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from bs4 import BeautifulSoup
import requests
from pprint import pprint
from tabulate import tabulate



DBENGINES = 'https://db-engines.com/en/ranking'
QUOTES = 'http://quotes.toscrape.com/search.aspx'


   
def bd_incrementos(umbral):
    
    r = requests.get(DBENGINES)
    soup = BeautifulSoup(r.content, 'html5lib')

    table = soup.find("table", attrs={"class": "dbi"})
    tr = table.find_all("tr")

    result = []

    for i in tr:
        td = i.find_all("td")
        if len(td) >= 5:
            name = td[1].text.strip()
            texto = td[4].text.strip().replace('%', '').replace(',', '.')
            try:
                incremento = float(texto)
            except ValueError:
                continue
            if incremento > umbral:
                result.append([name, f"{incremento}%"])

    return result

    #for tr in table.find_all("tr")[1:]
    
    


def citas_celebres(autor):
    """"""

def tags_por_autor():
    """"""

if __name__ == '__main__':
    print("This is only a test")
    # driver = webdriver.Chrome()   # Para Chrome
    tr = bd_incrementos(10)
    print(tabulate(tr, headers="firstrow", tablefmt="fancy_grid"))
  
   