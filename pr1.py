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

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


"""
Configuración de la página de DB-Engines para extraer información relevante.

Keys:
- url: URL de la página web a analizar.
- main_table_class: Clase CSS de la tabla principal que contiene los datos.
- main_table_header_class: Clase CSS de los encabezados de la tabla principal.
"""
DB_ENGINES_PAGE_CONFIG = {
    "url": "https://db-engines.com/en/ranking",
    "main_table_class": "dbi",
    "main_table_header_class": "dbi_header",
    "main_table_columns": {
        "database_name": 0,
        "main_model": 1,
        "annual_score_increase": -1,
    },
}

CITAS_CELEBRES_PAGE_CONFIG = {
    "url": "https://quotes.toscrape.com/search.aspx",
}

BASE_WAIT_DRIVER_TIME = 20


# TODO: we can cache here the HTML content to avoid multiple requests (this page doesn't change much)
def get_page_content_from_url(url: str) -> str:
    """Realiza una solicitud HTTP GET a la URL proporcionada y devuelve el contenido HTML de la página web.

    Parámetros:
        - url: str, la URL de la página web a la que se desea acceder.

    Retorna:
        - str: el contenido HTML de la página web.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")
        return ""


def bd_incrementos(umbral: float) -> list[tuple[str, str, float]]:
    """Retorna lista de tuplas (NOMBRE_BD, MODELO_PRINCIPAL_BD, INCREMENTO_PUNTUACIÓN_ANUAL)
    de las bases de datos con incremento anual mayor que umbral dado.

    Parámetros:
        - umbral: float, valor del umbral para filtrar las bases de datos.

    Retorna:
        - List[Tuple[str, str, float]]: lista de tuplas con la información
          de las bases de datos que cumplen el criterio.
    """
    page_content = get_page_content_from_url(DB_ENGINES_PAGE_CONFIG.get("url"))
    if not page_content:
        return []

    soup = BeautifulSoup(page_content, "html5lib")
    main_table = soup.find_all("table", DB_ENGINES_PAGE_CONFIG.get("main_table_class"))
    main_table_first_element = main_table[0]
    main_table_tbody = main_table_first_element.tbody
    main_table_rows = main_table_tbody.find_all("tr")

    tuples = []

    for row in main_table_rows:

        if row.find("td", class_=DB_ENGINES_PAGE_CONFIG.get("main_table_header_class")):
            continue

        main_table_td = row.find_all("td")
        main_table_th = row.find_all("th")

        # TODO: is this ok?
        if len(main_table_td) < 3 or len(main_table_th) < 2:
            continue

        database_name = (
            main_table_th[DB_ENGINES_PAGE_CONFIG["main_table_columns"]["database_name"]]
            .getText()
            .strip()
        )
        main_model_cell = main_table_th[
            DB_ENGINES_PAGE_CONFIG["main_table_columns"]["main_model"]
        ]
        main_model = list(main_model_cell.strings)[0].strip()
        increment = (
            main_table_td[
                DB_ENGINES_PAGE_CONFIG["main_table_columns"]["annual_score_increase"]
            ]
            .getText()
            .strip()
        )

        try:
            increment_value = float(increment.replace("±", ""))
        except ValueError:
            increment_value = 0.0

        if increment_value > umbral:
            tuples.append((database_name, main_model, increment_value))

    sorted_tuples = sorted(tuples, key=lambda x: x[2], reverse=True)
    return sorted_tuples


def obtener_autores(autor: str = None) -> list[str]:
    """Obtiene la lista de autores disponibles en la página de citas célebres.

    Parámetros:
        - autor: str, si se especifica, devuelve solo ese autor si existe.
                 Si es None, devuelve todos los autores.

    Retorna:
        - List[str]: lista de nombres de autores (uno o todos).
    """
    driver = webdriver.Chrome()
    driver.get(CITAS_CELEBRES_PAGE_CONFIG.get("url"))
    driver.implicitly_wait(BASE_WAIT_DRIVER_TIME)

    html_autor = driver.page_source
    soup_autor = BeautifulSoup(html_autor, "html5lib")
    select_author = soup_autor.css.select("select#author")
    options_authors = select_author[0].find_all("option")

    autores = [option.getText().strip() for option in options_authors[1:]]

    driver.close()

    if autor is not None:
        return [autor] if autor in autores else []

    return autores


def citas_celebres(autor: str, driver=None) -> dict[str, list[str]]:
    """Extrae citas célebres de un autor específico desde la página web configurada.

    Parámetros:
        - autor: str, nombre del autor cuyas citas se desean extraer.
        - driver: webdriver (opcional), si se proporciona reutiliza el driver existente.
                  Si es None, crea uno nuevo.

    Retorna:
        - Dict[str, List[str]]: diccionario con tags como keys y listas de citas como values.
    """
    close_driver = False
    if driver is None:
        driver = webdriver.Chrome()
        driver.get(CITAS_CELEBRES_PAGE_CONFIG.get("url"))
        driver.implicitly_wait(BASE_WAIT_DRIVER_TIME)
        close_driver = True

    element_author = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "author"))
    )
    element_author.click()
    element_author.send_keys(autor)
    element_author.click()

    # Wait for tag dropdown to be present after selecting author
    WebDriverWait(driver, BASE_WAIT_DRIVER_TIME).until(
        EC.presence_of_element_located((By.ID, "tag"))
    )

    html_for_tags = driver.page_source

    html_quotes = []

    soup_for_tags = BeautifulSoup(html_for_tags, 'html5lib')
    select_tag = soup_for_tags.css.select('select#tag')

    if not select_tag or len(select_tag) == 0:
        if close_driver:
            driver.close()
        return {}

    options = select_tag[0].find_all("option")

    quotes_by_tag = {}

    for option in options[1:]:
        driver.implicitly_wait(BASE_WAIT_DRIVER_TIME)

        tag = option.getText().strip()

        element_tag = WebDriverWait(driver, BASE_WAIT_DRIVER_TIME).until(
            EC.presence_of_element_located((By.ID, "tag"))
        )

        element_tag.click()
        element_tag.send_keys(tag)

        element_tag.click()

        element_button = WebDriverWait(driver, BASE_WAIT_DRIVER_TIME).until(
            EC.presence_of_element_located((By.NAME, "submit_button"))
        )

        element_button.click()

        driver.implicitly_wait(BASE_WAIT_DRIVER_TIME)

        WebDriverWait(driver, BASE_WAIT_DRIVER_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, "quote"))
        )

        WebDriverWait(driver, BASE_WAIT_DRIVER_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, "content"))
        )

        html_quotes.append([tag, driver.page_source])

    for tag, html_quote in html_quotes:
        soup_quote = BeautifulSoup(html_quote, "html5lib")
        results = soup_quote.find("div", class_="results")

        if not results:
            continue

        quotes = results.find_all("div", class_="quote")

        for quote in quotes:
            content = quote.find("span", class_="content")

            if not content:
                continue

            if tag not in quotes_by_tag:
                quotes_by_tag[tag] = []

            quotes_by_tag[tag].append(f"{content.getText().strip()}")

    if close_driver:
        driver.close()

    return quotes_by_tag


def tags_por_autor():
    """Cuenta el número de etiquetas asociadas a cada autor en la página de citas célebres.

    Retorna:
        - Dict[str, int]: diccionario con el número de etiquetas por autor.
    """
    driver = webdriver.Chrome()
    driver.get(CITAS_CELEBRES_PAGE_CONFIG.get("url"))
    driver.implicitly_wait(BASE_WAIT_DRIVER_TIME)

    html_autor = driver.page_source
    soup_autor = BeautifulSoup(html_autor, 'html5lib')
    select_author = soup_autor.css.select('select#author')
    options_authors = select_author[0].find_all("option")

    # Extract all author names first
    autores = [option.getText().strip() for option in options_authors[1:]]

    tags_per_author = {}

    for autor in autores:
        quotes_by_tag = citas_celebres(autor, driver)

        if autor not in tags_per_author:
            tags_per_author[autor] = 0

        tags_per_author[autor] = len(quotes_by_tag)

    driver.close()

    return tags_per_author


# print(bd_incrementos(2))
# print(citas_celebres("Jane Austen"))
print(tags_por_autor())
