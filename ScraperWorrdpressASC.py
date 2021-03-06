import base64
import json
import re
from datetime import datetime
import feedparser
from urllib.parse import urlparse, urljoin
import requests
import sys
import mysql.connector
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.parser import parse

mydb = mysql.connector.connect(
    host="167.86.120.98",
    port="3307",
    database="test_portales",
    user="eze_ellena",
    password="c3hdyX8Jvnua5ZBr"
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
def obtenerTextoCompletoRss(item,response, portal):

    try:

        TextoCompleto = item["content"][0]["value"]
        return TextoCompleto
    except Exception as e:

        TextoCompleto = obtenerTextoCompleto(response, portal[6])
        return TextoCompleto
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
    try:
        Descripcion = limpiar(re.sub("<.*?>", "", item["description"][0].value), mugre)
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripcion ", e)
def obtenerImagen(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                      'Firefox/55.0'}
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
def obtenerTextoCompleto(response,tag):
    try:
        TextoCompleto = eval(tag)
        TextoCompleto = str(TextoCompleto[0].contents)
        TextoCompleto = TextoCompleto.replace(r", ‘\n’,","").replace(r", ‘ ‘ "," ").replace("]","").replace("[","")\
            .replace(r"</p>, <p>","</p> <p>").replace(r", <p>","<p>").replace(r"</p>, ","</p>").replace(r"</div>, ","</div>")\
            .replace(r"'\n', <p>","<p>").replace(r", '\n'","").replace(r"</p>'\n'","</p>").replace(r"'\n'<p>","</p>")\
            .replace(r"'\n', <div","<div").replace(r"</div>'\n'","</div>").replace(r"</p>,","</p>").replace("</div>' '","</div>")\
            .replace(r"</p>' '<p>","</p><p>").replace(r"</p>' ',","</p>").replace(r", ' '"," ").replace(r"</script>, ","</script>")\
            .replace(r" , <script","<script").replace(r"</p>' '","</p>").replace(r"'\n', <h5>","<h5>").replace(r"</p> ' AddThis Advanced Settings above via filter on the_content ', ' AddThis Advanced Settings below via filter on the_content ', ' AddThis Advanced Settings generic via filter on the_content ', ' AddThis Share Buttons above via filter on the_content ', ' AddThis Share Buttons below via filter on the_content ', <div class='at-below-post addthis_tool' data-url='https://helvecia.com.uy/2021/04/04/colonia-supero-los-400-casos-de-covid-19/'></div>' AddThis Share Buttons generic via filter on the_content ', <div class='td-a-rec td-a-rec-id-content_bottom tdi_2 td_block_template_1'>","")\
            .replace(r"' '<p>","<p>").replace(r"</nav>, '/.pagination'","</nav>")
        return TextoCompleto
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
def obtenerImagenTotal(response):
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
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("a", {"data-v-da468678 href": ""}).text
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)



def funcionRss(portal):
    response = feedparser.parse(portal[7])
    if response:
        for item in response["items"]:
            try:
                fecha = item["pubDate"]
            except Exception as e:
                fecha = item["published"]

            dt = parse(fecha).strftime('%Y-%m-%d')

            hoy = datetime.today().strftime('%Y-%m-%d')
            print(dt)
            print(hoy)
            if dt == hoy:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0', }
                link = item["link"]
                response = requests.get(link, headers=headers).text
                try:
                    Titulo = obtenerTitulo(item)
                except Exception as e:
                    print("No se pudo obtener el Título ", e)

                try:
                    Descripcion = obtenerDescripcion(item)
                except Exception as e:
                    print("No se pudo obtener la Descripcion ", e)
                try:
                    TextoCompleto = obtenerTextoCompletoRss(item,response, portal)
                except Exception as e:
                    print("No se pudo obtener el texto completo ", e)

                try:
                    Imagen = obtenerImagenTotal(response)
                except Exception as e:
                    print("No se pudo obtener la Imagen ", e)
                if not Titulo or not Imagen:
                    continue
                else:
                        user = portal[1]
                        pythonapp = portal[3]
                        url = portal[4]
                        data_string = user + ':' + pythonapp
                        token = base64.b64encode(data_string.encode())
                        headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
                        imgsrc = Imagen
                        try:
                            mycursor = mydb.cursor()
                            sql = "INSERT INTO noticias_enviadas_wordpress (link, titulo, descripcion,tema,campaña,nombreWordPress) VALUES (%s, %s, %s, %s, %s, %s)"
                            val = (link, Titulo, Descripcion, "", "", url)
                            mycursor.execute(sql, val)
                            mydb.commit()
                            if TextoCompleto is None:
                                TextoCompleto  = ""
                            try:

                                post = {'date': str(datetime.now() + timedelta(hours=-3)),
                                        'title': Titulo,
                                        'slug': 'rest-api-1',
                                        'status': 'publish',
                                        'content': Descripcion + '\n\n<img align="middle" src=' + imgsrc + '>\n' + str(TextoCompleto),
                                        'author': '1',
                                        'format': 'standard',
                                        'post_tag': "",
                                        'category': ""
                                        }
                                r = requests.post(url + '/posts', headers=headers, json=post)

                                print('Your post is published on ' +
                                      json.loads(r.content.decode('utf-8'))['link'])

                            except Exception as e:
                                print("Error al Obtener portales ", e)

                        except Exception as e:
                            print("Error al ejecutar la consulta")

def funcionLink(portal):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                      'Firefox/55.0'}
    links = get_all_website_links(portal[5])
    links = list(links)
    format_strings = ','.join(['%s'] * len(links))
    try:
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT * FROM noticias_enviadas_wordpress where link IN (%s)" % format_strings,
            tuple(links))
        innoticia = mycursor.fetchall()
        linkbasededatos = []
        for j in innoticia:
            linkbasededatos.append(j[0])
        for i in links[:]:
            if i in linkbasededatos:
                links.remove(i)
    except Exception as e:
        print("")
    try:
        format_strings2 = ','.join(['%s'] * len(links))
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT * FROM noticias_basuras_wordpress where link IN (%s)" % format_strings2,
            tuple(links))
        innoticiaBasura = mycursor.fetchall()
        linkbasededatosBasura = []
        for j in innoticiaBasura:
            linkbasededatosBasura.append(j[1])
        for i in links[:]:
            if i in linkbasededatosBasura:
                links.remove(i)
    except Exception as e:
        print("")


    for link in links:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                          'Firefox/55.0'}
        response = requests.get(link, headers=headers).text
        try:
            Titulo = obtenerTituloLink(response)
        except Exception as e:
            print("No se pudo obtener el Título ", e)
        try:
            Descripcion = obtenerDescripcionLink(response)
            if Descripcion == "" or Descripcion == '':
                Descripcion = "."
            if not Descripcion:
                Descripcion = "."
        except Exception as e:
            print("No se pudo obtener la Descripcion ", e)
        try:
            Imagen = obtenerImagenLink(response)
        except Exception as e:
            print("No se pudo obtener la Imagen ", e)
        try:
            TextoCompleto = obtenerTextoCompletoLink(response, portal[6])
        except Exception as e:
            print("No se pudo obtener la Imagen ", e)
        try:
            # Categoria = obtenerCategoriaLink(response)
            Categoria = 'actualidad'
        except Exception as e:
            print("No se pudo obtener la Categoria ", e)
            Categoria = 'actualidad'
        try:
            # Tags = obtenerTagsLink(response)

            Tags = 'Actualidad'
        except Exception as e:
            print("No se pudo obtener el Tag ", e)
            Tags = 'Actualidad'

        if not Titulo or not Descripcion or not Imagen or not TextoCompleto:
            try:
                mycursor = mydb.cursor()
                sql = "INSERT INTO noticias_basuras_wordpress (portal,link,nombreWordPress) VALUES (%s, %s, %s)"
                val = (portal[5], link, portal[4])
                mycursor.execute(sql, val)
                mydb.commit()
            except Exception as e:
                print("Error al Obtener portales ", e)
            continue
        else:
            user = portal[1]
            pythonapp = portal[3]
            url = portal[4]
            data_string = user + ':' + pythonapp
            token = base64.b64encode(data_string.encode())
            headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
            imgsrc = Imagen
            try:
                mycursor = mydb.cursor()
                sql = "INSERT INTO noticias_enviadas_wordpress (link, titulo, descripcion,tema,campaña,nombreWordPress) " \
                      "VALUES (%s, %s, %s, %s, %s, %s)"
                val = (link, Titulo, Descripcion, "", "", url)
                mycursor.execute(sql, val)
                mydb.commit()
                try:

                    post = {'date': str(datetime.now() + timedelta(hours=-3)),
                            'title': Titulo,
                            'slug': 'rest-api-1',
                            'status': 'publish',
                            'content': Descripcion + '\n\n<img align="middle" src=' + imgsrc + '>\n' + TextoCompleto,
                            'author': '1',
                            'format': 'standard',
                            'post_tag': Tags,
                            'category': Categoria
                            }
                    r = requests.post(url + '/posts', headers=headers, json=post)

                    print('Your post is published on ' + json.loads(r.content.decode('utf-8'))['link'])

                except Exception as e:
                    print("Error al Obtener portales ", e)
            except Exception as e:
                print("Error al Obtener portales ", e)

def obtenerTituloLink(response):
    Titulo = ""
    try:
        Titulo = BeautifulSoup(response, "html.parser").find("meta", {"name": "twitter:title"})[
            "content"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = BeautifulSoup(response, "html.parser").find("meta", {"property": "og:title"})[
            "content"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = \
            json.loads(BeautifulSoup(response, "html.parser").find("script", {
                "type": 'application/ld+json'}).string)[0][
                "headline"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = \
            json.loads(BeautifulSoup(response, "html.parser").find("script", {
                "type": 'application/ld+json'}).string)[
                "headline"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = BeautifulSoup(response, "html.parser").find("p", {"data-v-da468678 class": 'titulo'})
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
def obtenerDescripcionLink(response):
    Descripcion = ""
    try:
        Descripcion = \
        BeautifulSoup(response, "html.parser").find("meta", {"name": "twitter:description"})["content"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripción ", e)
    try:
        Descripcion = \
        BeautifulSoup(response, "html.parser").find("meta", {"property": "og:description"})["content"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripción ", e)
    try:
        Descripcion = \
            json.loads(BeautifulSoup(response, "html.parser").find("script", {
                "type": 'application/ld+json'}).string)[0][
                "description"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripción ", e)
    try:
        Descripcion = \
            json.loads(BeautifulSoup(response, "html.parser").find("script", {
                "type": 'application/ld+json'}).string)[
                "description"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripción ", e)
    try:
        Descripcion = \
            BeautifulSoup(response, "html.parser").find("p", {"data-v-da468678 class": 'anticipo'})
        return Descripcion
    except Exception as e:
        print("No se pudo obtener la Descripción ", e)
def obtenerImagenLink(response):
    Imagen = ""
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"name": "twitter:image"})[
            "content"]
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("meta", {"property": "og:image"})[
            "content"]
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
    try:
        Imagen = BeautifulSoup(response, "html.parser").find("a", {"data-v-da468678 href": ""}).text
        return Imagen
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
def obtenerTextoCompletoLink(response, tag):
    try:
        TextoCompleto = eval(tag)
        TextoCompleto = str(TextoCompleto[0].contents)
        TextoCompleto = TextoCompleto.replace(r", ‘\n’,", "").replace(r", ‘ ‘ ", " ").replace("]",
                                                                                              "").replace(
            "[", "") \
            .replace(r"</p>, <p>", "</p> <p>").replace(r", <p>", "<p>").replace(r"</p>, ",
                                                                                "</p>").replace(
            r"</div>, ", "</div>") \
            .replace(r"'\n', <p>", "<p>").replace(r", '\n'", "").replace(r"</p>'\n'", "</p>").replace(
            r"'\n'<p>", "</p>") \
            .replace(r"'\n', <div", "<div").replace(r"</div>'\n'", "</div>").replace(r"</p>,",
                                                                                     "</p>").replace(
            "</div>' '", "</div>") \
            .replace(r"</p>' '<p>", "</p><p>").replace(r"</p>' ',", "</p>").replace(r", ' '",
                                                                                    " ").replace(
            r"</script>, ", "</script>") \
            .replace(r" , <script", "<script").replace(r"</p>' '", "</p>").replace(r"'\n', <h5>",
                                                                                   "<h5>").replace(
            r"</p> ' AddThis Advanced Settings above via filter on the_content ', ' AddThis Advanced Settings below via filter on the_content ', ' AddThis Advanced Settings generic via filter on the_content ', ' AddThis Share Buttons above via filter on the_content ', ' AddThis Share Buttons below via filter on the_content ', <div class='at-below-post addthis_tool' data-url='https://helvecia.com.uy/2021/04/04/colonia-supero-los-400-casos-de-covid-19/'></div>' AddThis Share Buttons generic via filter on the_content ', <div class='td-a-rec td-a-rec-id-content_bottom tdi_2 td_block_template_1'>",
            "") \
            .replace(r"' '<p>", "<p>").replace(r"</nav>, '/.pagination'", "</nav>")
        return TextoCompleto
    except Exception as e:
        print("No se pudo obtener la Imagen ", e)
def obtenerTagsLink(response):
    try:
        Tags = BeautifulSoup(response, "html.parser").find("meta", {"name": "keywords"})
        return Tags
    except Exception as e:
        print("No se pudo obtener el tag ", e)
def obtenerCategoriaLink(response):
    try:
        Tags = BeautifulSoup(response, "html.parser").find("meta", {"name": "keywords"})
        return Tags
    except Exception as e:
        print("No se pudo obtener el tag ", e)

if __name__ == "__main__":

        try:
            while True:
                try:
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM Wordpress order by dominio asc"
                    mycursor.execute(sql)
                    sql = mycursor.fetchall()
                    for portal in sql:

                        try:
                            if portal[7] is not None:
                                try:
                                    funcionRss(portal)
                                except Exception as e:
                                    print("Error al ejecutar la consulta")
                                    continue
                            else:
                                try:
                                    funcionLink(portal)
                                except Exception as e:
                                    print("Error al ejecutar la consulta")
                                    continue

                        except Exception as e:
                            print("Error al ejecutar la consulta")
                            continue
                except Exception as e:
                    print("Error al ejecutar la consulta")
                    continue
        except Exception as e:
            print("Error al ejecutar la consulta")
