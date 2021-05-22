import json
from datetime import datetime
from urllib.parse import urlparse, urljoin
import requests
import sys
import mysql.connector
from bs4 import BeautifulSoup
from collections import OrderedDict
mydb = mysql.connector.connect(
  host="167.86.120.98",
  port="3307",
  database="test_portales",
  user="eze_ellena",
  password="c3hdyX8Jvnua5ZBr"
)
mydbEze = mysql.connector.connect(
  host="167.86.120.98",
  port="3307",
  database="test_portales",
  user="eze_ellena",
  password="c3hdyX8Jvnua5ZBr"
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
        print("")
    try:
        Titulo = BeautifulSoup(response, "html.parser").find("meta", {"property":"og:title"})["content"]
        return Titulo
    except Exception as e:
        print("")
    try:
        Titulo = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[0]["headline"]
        return Titulo
    except Exception as e:
        print("")
    try:
        Titulo = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)["headline"]
        return Titulo
    except Exception as e:
        print("")
def obtenerDescripcion(response):
    Descripcion = ""
    try:
        Descripcion = BeautifulSoup(response, "html.parser").find("meta", {"name":"twitter:description"})["content"]
        if Descripcion != "":
            return Descripcion
    except Exception as e:
        print("")
    try:
        Descripcion = BeautifulSoup(response, "html.parser").find("meta", {"property":"og:description"})["content"]
        if Descripcion != "":
            return Descripcion
    except Exception as e:
        print("")
    try:
        Descripcion = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[0]["description"]
        if Descripcion != "":
            return Descripcion
    except Exception as e:
        print("")
    try:
        Descripcion = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)["description"]
        if Descripcion != "":
            return Descripcion
    except Exception as e:
        print("")
def obtenerImagen(response):
    Imagen = ""
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"name":"twitter:image"})["content"]
        return Imagen
    except Exception as e:
        print("")
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"property":"og:image"})["content"]
        return Imagen
    except Exception as e:
        print("")
def obtenerFechaPublicacion(response):
    FechaPublicacion = ""
    try:
        FechaPublicacion = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[0]["datePublished"]
        return FechaPublicacion
    except Exception as e:
        print("")
    try:
        FechaPublicacion = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)["datePublished"]
        return FechaPublicacion
    except Exception as e:
        print("")
    try:
        FechaPublicacion = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)["@graph"][2]["datePublished"]
        return FechaPublicacion
    except Exception as e:
        print("")
    try:
        FechaPublicacion = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)["@graph"][4]["datePublished"]
        return FechaPublicacion
    except Exception as e:
        print("")
    try:
        FechaPublicacion = json.loads(BeautifulSoup(response, "html.parser").find_all("script", {"type": 'application/ld+json'})[1].string)["datePublished"]
        return FechaPublicacion
    except Exception as e:
        print("")
    try:
        FechaPublicacion = BeautifulSoup(response, "html.parser").find("meta", {"property":"article:published_time"})["content"]
        return FechaPublicacion
    except Exception as e:
        print("")
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
                    mycursor = mydb.cursor()
                    sql = "SELECT url, id_provincia FROM portales where id_provincia = "+ Id_Provincia +""
                    mycursor.execute(sql)
                    sql = mycursor.fetchall()
                    for portal in sql:
                        try:
                            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                                                     'Firefox/55.0'}
                            links = get_all_website_links(portal[0])
                            links = list(links)
                            format_strings = ','.join(['%s'] * len(links))
                            try:
                                mycursor = mydb.cursor()
                                mycursor.execute("SELECT * FROM todas_las_noticias where link IN (%s)" % format_strings, tuple(links))
                                innoticia = mycursor.fetchall()
                                linkbasededatos = []
                                for j in innoticia:
                                    linkbasededatos.append(j[0])
                                for i in links[:]:
                                    if i in linkbasededatos:
                                        links.remove(i)
                            except Exception as e:
                                print("")

                            for link in links:
                                response = requests.get(link, headers=headers).text
                                try:
                                    Titulo = obtenerTitulo(response)
                                except Exception as e:
                                    print("")
                                try:
                                    Descripcion = obtenerDescripcion(response)
                                except Exception as e:
                                    print("")
                                try:
                                    Imagen = obtenerImagen(response)
                                except Exception as e:
                                    print("")

                                try:
                                    fecha = obtenerFechaPublicacion(response)
                                    mycursor = mydb.cursor()
                                    sql = "INSERT INTO todas_las_noticias (link,fecha,titulo,copete,texto,medio,provincia,imagen) " \
                                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
                                    val = (link, fecha, Titulo, Descripcion, "", portal[0], portal[1],Imagen)
                                    mycursor.execute(sql, val)
                                    mydb.commit()
                                    print("insertó correctamente el link: " + link + "")
                                except Exception as e:
                                    print("error" + link + "" + str(e.msg) + "")
                        except Exception as e:
                            print("Error al ejecutar la consulta")
                except Exception as e:
                    print("Error al ejecutar la consulta")
        except Exception as e:
            print("Error al ejecutar la consulta")