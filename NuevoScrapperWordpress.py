import feedparser as fp
import json
import newspaper
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from time import mktime
import mysql.connector
import base64
from datetime import datetime, timedelta


mydb = mysql.connector.connect(
    host="10.3.0.125",
    port="3307",
    database="portales",
    user="root",
    password="terminator9519"
)
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

while True:
    try:

        mycursor = mydb.cursor()
        sql = "SELECT * FROM Wordpress order by dominio desc"
        mycursor.execute(sql)
        sql = mycursor.fetchall()
        for portal in sql:
            try:
                if portal[7] is not None:
                    d = fp.parse(portal[7])
                    for entry in d.entries:
                        # Check if publish date is provided, if no the article is skipped.
                        # This is done to keep consistency in the data and to keep the script from crashing.
                        if hasattr(entry, 'published'):


                            try:
                                content = Article(entry.link)
                                content.download()
                                content.parse()
                            except Exception as e:
                                # If the download for some reason fails (ex. 404) the script will continue downloading
                                # the next article.
                                print(e)
                                print("continuing...")
                                continue
                            try:
                                twitter = content.meta_data["twitter"]
                            except Exception as e:
                                print("twitter")
                            try:
                                og = content.meta_data["og"]
                            except Exception as e:
                                print("og")
                            link = entry.link

                            try:
                                Titulo = content.title
                                if Titulo is None or "":
                                    Titulo = twitter["title"]
                            except Exception as e:
                                print("")

                            try:
                                TextoCompleto = content.text
                            except Exception as e:
                                print("")
                            try:
                                fecha = entry.published_parsed
                                fecha = datetime.fromtimestamp(mktime(fecha)).isoformat()
                            except Exception as e:
                                print("")
                            try:
                                Imagen = content.top_image
                                if Imagen is None or '':
                                    Imagen = twitter["image"]
                                    if Imagen is None or '':
                                        Imagen = og["image"]
                            except Exception as e:
                                print("")
                            try:
                                Descripcion = entry.summary
                                if Descripcion is None or '':
                                    Descripcion = twitter["description"]
                                    if Descripcion is None or '':
                                        Descripcion = og["description"]
                            except Exception as e:
                                print("")
                            if not Titulo or not Imagen:
                                continue
                            else:
                                user = portal[1]
                                pythonapp = portal[3]
                                url = portal[4]
                                data_string = user + ':' + pythonapp
                                token = base64.b64encode(data_string.encode())
                                headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
                                try:
                                    mycursor = mydb.cursor()
                                    sql = "INSERT INTO noticias_enviadas_wordpress (link, titulo, descripcion,tema,campaña,nombreWordPress) VALUES (%s, %s, %s, %s, %s, %s)"
                                    val = (link, Titulo, Descripcion, "", "", url)
                                    mycursor.execute(sql, val)
                                    mydb.commit()
                                    if TextoCompleto is None:
                                        TextoCompleto = ""
                                    try:

                                        post = {'date': str(datetime.now() + timedelta(hours=-3)),
                                                'title': Titulo,
                                                'slug': 'rest-api-1',
                                                'status': 'publish',
                                                'content': Descripcion + '\n\n<img align="middle" src=' + Imagen + '>\n' + str(
                                                    TextoCompleto),
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
                                    print("insert",e)
                else:

                    print("Building site for ", portal[5])
                    paper = newspaper.build(portal[5], memoize_articles=False)

                    for content in paper.articles:

                        try:
                            content.download()
                            content.parse()
                        except Exception as e:
                            print(e)
                            print("continuing...")
                            continue
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                                          'Firefox/55.0'}
                        try:
                            a = Article(content.url, keep_article_html=True)
                            a.download()
                            a.parse()
                        except Exception as e:
                            print("article",e)
                        try:
                            twitter = content.meta_data["twitter"]
                        except Exception as e:
                            print("twitter")
                        try:
                            og = content.meta_data["og"]
                        except Exception as e:
                            print("og")

                        response = requests.get(content.url, headers=headers).text
                        link = content.url
                        try:
                            if content.title is not None or not "":
                                Titulo = content.title
                            elif a.title is not None or not "":
                                Titulo = a.title
                            else:
                                Titulo = obtenerTitulo(response)
                        except Exception as e:
                            try:
                                Titulo = a.title
                            except Exception as e:
                                Titulo = obtenerTitulo(response)

                        try:
                            if content.text is not None or not "":
                                TextoCompleto = content.text
                            elif a.text is not None or not "":
                                TextoCompleto = a.text
                            else:
                                TextoCompleto = obtenerTitulo(response)
                        except Exception as e:
                            try:
                                TextoCompleto = a.text
                            except Exception as e:
                                TextoCompleto = obtenerDescripcion(response)

                        try:
                            if content.publish_date is not None or not "":
                                fecha = content.publish_date.isoformat()
                            elif a.publish_date is not None or not "":
                                fecha = a.publish_date.isoformat()
                            else:
                                fecha = obtenerFechaPublicacion(response)
                        except Exception as e:
                            try:
                                fecha = a.publish_date.isoformat()
                            except Exception as e:
                                fecha = obtenerFechaPublicacion(response)

                        try:
                            if content.top_image is not None or not "":
                                Imagen = content.top_image
                            elif a.top_image is not None or not "":
                                Imagen = a.top_image
                            else:
                                Imagen = obtenerFechaPublicacion(content.url)
                        except Exception as e:
                            try:
                                Imagen = a.top_image
                            except Exception as e:
                                Imagen = obtenerImagen(content.url)

                        try:
                            Descripcion = a.summary
                            if Descripcion is None or '':
                                Descripcion = twitter["description"]
                                if Descripcion is None or '':
                                    Descripcion = og["description"]
                        except Exception as e:
                            print("",e)


                        if not Titulo or not Imagen:
                            continue
                        else:
                            user = portal[1]
                            pythonapp = portal[3]
                            url = portal[4]
                            data_string = user + ':' + pythonapp
                            token = base64.b64encode(data_string.encode())
                            headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
                            try:
                                mycursor = mydb.cursor()
                                sql = "INSERT INTO noticias_enviadas_wordpress (link, titulo, descripcion,tema,campaña,nombreWordPress) VALUES (%s, %s, %s, %s, %s, %s)"
                                val = (link, Titulo, Descripcion, "", "", url)
                                mycursor.execute(sql, val)
                                mydb.commit()
                                if TextoCompleto is None:
                                    TextoCompleto = ""
                                try:

                                    post = {'date': str(datetime.now() + timedelta(hours=-3)),
                                            'title': Titulo,
                                            'slug': 'rest-api-1',
                                            'status': 'publish',
                                            'content': Descripcion + '\n\n<img align="middle" src=' + Imagen + '>\n' + str(
                                                TextoCompleto),
                                            'author': '1',
                                            'format': 'standard',
                                            'post_tag': "",
                                            'category': ""
                                            }
                                    r = requests.post(url + '/posts', headers=headers, json=post)

                                    print('Your post is published on ' +
                                          json.loads(r.content.decode('utf-8'))['link'] + r.content.decode()["status"])

                                except Exception as e:
                                    print("Error al insertar wordpress ", e)

                            except Exception as e:
                                print("insert",e)

            except Exception as e:
                print("",e)
    except Exception as e:
        print("",e)
