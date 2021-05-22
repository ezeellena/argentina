import json

import requests
import mysql.connector
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

mydb = mysql.connector.connect(
    host="167.86.120.98",
    port="3307",
    database="test_portales",
    user="root",
    password="dalas.2009"
)
test_eze = mysql.connector.connect(
    host="167.86.120.98",
    port="3307",
    database="TestEze",
    user="root",
    password="dalas.2009"
)

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def obtenerTitulo(response):
    Titulo = ""
    try:
        Titulo = BeautifulSoup(response, "html.parser").find("meta", {"name": "twitter:title"})["content"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = BeautifulSoup(response, "html.parser").find("meta", {"property": "og:title"})["content"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = \
        json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[0][
            "headline"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = \
        json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[
            "headline"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)


def obtenerDescripcion(response):
    Descripcion = ""
    try:
        Descripcion = BeautifulSoup(response, "html.parser").find("meta", {"name": "twitter:description"})["content"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Descripcion = BeautifulSoup(response, "html.parser").find("meta", {"property": "og:description"})["content"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Descripcion = \
        json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[0][
            "description"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Descripcion = \
        json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[
            "description"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener el Título ", e)


def obtenerImagen(response):
    Imagen = ""
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"name": "twitter:image"})["content"]
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"property": "og:image"})["content"]
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)


def get_all_website_links(Portal):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()

    internal_urls = set()
    external_urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(Portal).netloc
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0', }
    soup = BeautifulSoup(requests.get(Portal, headers=headers).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(Portal, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            continue
        # print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return internal_urls


if __name__ == "__main__":

    try:
        try:
            mycursor = mydb.cursor()
            sql = "SELECT url from portales"
            mycursor.execute(sql)
            sql = mycursor.fetchall()
        except Exception as e:
            print("Error al ejecutar la consulta")
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                                 'Firefox/55.0'}
        response = requests.get(Portal["url"], headers=headers).text
        links = get_all_website_links(Portal["url"])
        links = list(links)
        linksNUevos = []
        for i in links:
            if i not in sql:
                linksNUevos.append(i)
        print(linksNUevos)
        for link in links:
            try:
                Titulo = obtenerTitulo(response)
            except Exception as e:
                print("No se pudo obtener el Título ", e)
            try:
                Descripcion = obtenerDescripcion(response)
            except Exception as e:
                print("No se pudo obtener la Descripcion ", e)
            try:
                Imagen = obtenerImagen(response)
            except Exception as e:
                print("No se pudo obtener la Imagen ", e)

            if not Titulo or not Descripcion or not Imagen:
                break


    except Exception as e:
        print("Error al Obtener portales ", e)
