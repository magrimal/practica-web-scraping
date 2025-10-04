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



def citas_celebres(autor):
    """"""

def tags_por_autor():
    """"""

bd_incrementos(2)