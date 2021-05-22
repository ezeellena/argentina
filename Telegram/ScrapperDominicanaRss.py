import json
import re
from datetime import datetime
import feedparser
from urllib.parse import urlparse, urljoin
import requests
import sys
import mysql.connector
from bs4 import BeautifulSoup

mydb = mysql.connector.connect(
  host="10.3.0.125",
  port="3307",
  database="test_portales",
  user="eze_ellena",
  password="L9vMKWedYEzcBxdy"
)
mydbEze = mysql.connector.connect(
  host="10.3.0.125",
  port="3307",
  database="test_portales",
  user="eze_ellena",
  password="L9vMKWedYEzcBxdy"
)
mugre = ["rdquo;","&amp;","&gt",".ar",".com",";>>",";>","<br","&quot;","xmlns=http://www.w3.org/1999/>","<\n", "\n>","<<p>","<p>","</p","xmlns=http://www.w3.org/1999/>","xmlns=http://www.w3.org/1999/>","<br />","CDATA", "</div>>", "<div>", "</div>","%>", "<iframe>", "</iframe>", "100%", "<div", "http://w3.org/","xmlms","xhtml", ";>","]",'"',"'"]

def limpiar(texto, mugre):
    for m in mugre:
        texto = texto.replace(m,"")
    return texto
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
def obtenerTitulo(item):

    try:
        Titulo = item["title"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)

def obtenerDescripcion(item):

    try:
        Descripcion = limpiar(re.sub("<.*?>", "", item["summary"]), mugre)
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripcion ", e)
    try:
        Descripcion = limpiar(re.sub("<.*?>", "", item["content"][0].value), mugre)
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripcion ", e)

def obtenerImagen(link):
    response = requests.get(link, headers=headers).text
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"name":"twitter:image"})["content"]
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"property":"og:image"})["content"]
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
def obtenerFechaPublicacion(item):
    try:
        FechaPublicacion = item["published"]
        return FechaPublicacion
    except Exception as e:
        print("No se pudo obtener la FechaPublicacion ", e)
    try:
        FechaPublicacion = item["updated"]
        return FechaPublicacion
    except Exception as e:
        print("No se pudo obtener la FechaPublicacion ", e)
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0', }
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
            while True:
                try:
                    if len(sys.argv) > 1:
                        Id_Provincia = sys.argv[1]
                    #Id_Provincia = "5"
                    mycursor = mydb.cursor()
                    sql = "SELECT url, url_rss, id_provincia FROM portales where id_provincia = "+Id_Provincia+" order by  url desc"
                    mycursor.execute(sql)
                    sql = mycursor.fetchall()
                    for portal in sql:
                        try:
                            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                                                     'Firefox/55.0'}
                            response = feedparser.parse(portal[1])
                            if response:
                                for item in response["items"]:
                                    link = item["link"]
                                    try:
                                        mycursor = mydb.cursor()
                                        innoticia = "SELECT * FROM todas_las_noticias where link = '" + link + "'"
                                        mycursor.execute(innoticia)
                                        innoticia = mycursor.fetchall()
                                    except Exception as e:
                                        print("")
                                    try:
                                        mycursor = mydb.cursor()
                                        innoanda = "select * from portales_no_andan_scrap_dominicana WHERE url_link = '" + link + "'"
                                        mycursor.execute(innoanda)
                                        innoanda = mycursor.fetchall()
                                    except Exception as e:
                                        print("")
                                    cantidad = len(innoticia)
                                    cantidad2 = len(innoanda)
                                    if cantidad != 0 or cantidad2 != 0:
                                        print("ya se encuentra enla base")
                                    else:

                                        try:
                                            Titulo = obtenerTitulo(item)
                                        except Exception as e:
                                            print("No se pudo obtener el Título ", e)
                                        try:
                                            Descripcion = obtenerDescripcion(item)
                                        except Exception as e:
                                            print("No se pudo obtener la Descripcion ", e)
                                        try:
                                            Imagen = obtenerImagen(link)
                                        except Exception as e:
                                            print("No se pudo obtener la Imagen ", e)

                                        if not Titulo or not Descripcion:
                                            try:
                                                mycursorEze = mydbEze.cursor()
                                                sql = "INSERT INTO portales_no_andan_scrap_dominicana (url_portal, url_link) " \
                                                      "VALUES (%s, %s) "
                                                val = (portal[1], link)
                                                mycursorEze.execute(sql, val)
                                                mydbEze.commit()
                                                print("insertó correctamente el link: " + link + "")
                                            except Exception as e:
                                                print("El Link ya fue guardado: " + link + "" + str(e.msg) + "")
                                        else:
                                            try:
                                                fecha = obtenerFechaPublicacion(item)
                                                mycursor = mydb.cursor()
                                                sql = "INSERT INTO todas_las_noticias (link,fecha,titulo,copete,texto,medio,provincia,imagen) " \
                                                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
                                                val = (link, fecha, Titulo, Descripcion, "", portal[1], portal[2],Imagen)
                                                mycursor.execute(sql, val)
                                                mydb.commit()
                                                print("insertó correctamente el link: " + link + "")
                                            except Exception as e:
                                                print("El Link ya fue guardado: " + link + "" + str(e.msg) + "")

                        except Exception as e:
                            print("Error al ejecutar la consulta")
                except Exception as e:
                    print("Error al ejecutar la consulta")
        except Exception as e:
            print("Error al ejecutar la consulta")