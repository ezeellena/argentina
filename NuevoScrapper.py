import sys

import feedparser as fp
import json

from dateutil.parser import parse
import newspaper
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from time import mktime
from datetime import datetime
import mysql.connector

# Set the limit for number of articles to download
LIMIT = 4

data = {}
data['newspapers'] = {}
count = 1
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
        """
        mycursor = mydb.cursor()
        sql = "SELECT url, id_provincia FROM portales where id_provincia = '20'"
        mycursor.execute(sql)
        sql = mycursor.fetchall()
        for portal in sql:
            d = fp.parse('https://bumerangnews.com/feed/')
            newsPaper = {
                "link": "https://bumerangnews.com/feed/",
                "category": [],
                "feed": "https://bumerangnews.com/feed/",
                "articles": []
            }
            for entry in d.entries:
                # Check if publish date is provided, if no the article is skipped.
                # This is done to keep consistency in the data and to keep the script from crashing.
                if hasattr(entry, 'published'):
                    article = {}


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
                    twitter = content.meta_data["twitter"]
                    og = content.meta_data["og"]
                    article['link'] = entry.link

                    try:
                        article['title'] = content.title
                        if article['title'] is None or "":
                            article['title'] = twitter["title"]
                    except Exception as e:
                        print("")

                    try:
                        article['text'] = content.text
                    except Exception as e:
                        print("")
                    try:
                        date = entry.published_parsed
                        article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                    except Exception as e:
                        print("")
                    try:
                        article['top_image'] = content.top_image
                        if article['top_image'] is None or '':
                            article['top_image'] = twitter["image"]
                            if article['top_image'] is None or '':
                                article['top_image'] = og["image"]
                    except Exception as e:
                        print("")
                    try:
                        article['authors'] = content.authors
                    except Exception as e:
                        print(e)
                    try:
                        article['summary'] = a.summary
                        if article['summary'] is None or '':
                            article['summary'] = twitter["description"]
                            if article['summary'] is None or '':
                                article['summary'] = og["description"]
                    except Exception as e:
                        print("")
                    try:
                        article['keywords'] = content.keywords
                    except Exception as e:
                        print("")
                    newsPaper['articles'].append(article)
        """

        mycursor = mydb.cursor()
        sql = "SELECT url, id_provincia FROM portales where id_provincia = '20'"
        mycursor.execute(sql)
        sql = mycursor.fetchall()

        for portal in sql:
            try:
                print("Building site for ", portal[0])
                paper = newspaper.build(portal[0], memoize_articles=False)
                article = {}
                newsPaper = {
                    "articles": []
                }
                noneTypeCount = 0
            except Exception as e:
                print("ERROR al construir portal ",portal[0] + e)

            """
            for category in paper.category_urls():
                if category is not None or not "":
                    print(category)
                try:
                    newsPaper["category"].append(category)
                except Exception as e:
                    print("")
            for feed_url in paper.feed_urls():
                if feed_url is not None or not "":
                    print(feed_url)
                try:
                    newsPaper["feed"].append(feed_url)
                except Exception as e:
                    print("")
            """
            lista = []
            if len(paper.articles) == 0:
                print("No se obtuvieron articulos", portal[2])
            if len(paper.articles) > 0:
                for url in paper.articles:
                    lista.append(url[0])

                format_strings = ','.join(['%s'] * len(paper.articles))
                medio = portal[0]
                mycursor = mydb.cursor()
                sqlnot = "SELECT *  FROM todas_las_noticias_nuevas WHERE medio like '%" + medio + "%' and link IN (" + format_strings + ")"
                val = lista
                mycursor.execute(sqlnot, val)
                sqlnot = mycursor.fetchall()
                for remove in sqlnot:
                    lista.remove(remove[0])
                if len(lista) > 0:
                    for content in paper.articles:

                        try:
                            #print(paper.size())
                            content.download()
                            content.parse()
                        except Exception as e:
                            print(e)
                            print("continuing...")
                            continue
                        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                                                 'Firefox/55.0'}
                        try:
                            a = Article(content.url, keep_article_html=True)
                            a.download()
                            a.parse()
                        except Exception as e:
                            continue
                        response = requests.get(content.url, headers=headers, timeout=10).text

                        try:
                            if content.title is not None or not "":
                                article['title'] = content.title
                            elif a.title is not None or not "":
                                article['title'] = a.title
                            else:
                                article['title'] = obtenerTitulo(response)
                        except Exception as e:
                            try:
                                article['title'] = a.title
                            except Exception as e:
                                article['title'] = obtenerTitulo(response)
                        print(article['title'])
                        try:
                            if content.text is not None or not "":
                                article['text'] = content.text
                            elif a.text is not None or not "":
                                article['text'] = a.text
                            else:
                                article['text'] = obtenerTitulo(response)
                        except Exception as e:
                            try:
                                article['text'] = a.text
                            except Exception as e:
                                article['text'] = obtenerDescripcion(response)
                        print(article['text'])

                        try:
                            if content.publish_date is not None or not "":
                                article['publish_date'] = content.publish_date
                            elif a.publish_date is not None or not "":
                                article['publish_date'] = a.publish_date
                            else:
                                article['publish_date'] = obtenerFechaPublicacion(response)
                        except Exception as e:
                            try:
                                article['publish_date'] = a.publish_date
                            except Exception as e:
                                article['publish_date'] = obtenerFechaPublicacion(response)
                        print(article['publish_date'])

                        try:
                            if content.top_image is not None or not "":
                                article['top_image'] = content.top_image
                            elif a.top_image is not None or not "":
                                article['top_image'] = a.top_image
                            else:
                                article['top_image'] = obtenerImagen(content.url)
                        except Exception as e:
                            try:
                                article['top_image'] = a.top_image
                            except Exception as e:
                                article['top_image'] = obtenerImagen(content.url)
                        print(article['top_image'])

                        try:
                            if content.authors is not None or not "":
                                article['authors'] = content.authors
                            elif a.authors is not None or not "":
                                article['authors'] = a.authors
                            else:
                                article['authors'] = ""
                        except Exception as e:
                            try:
                                article['authors'] = a.authors
                            except Exception as e:
                                article['authors'] = ""
                        print(article['authors'])

                        try:
                            article['summary'] = a.summary
                        except Exception as e:
                            print("summary",e)
                        try:
                            article['keywords'] = a.keywords
                        except Exception as e:
                            print("keywords",e)

                        print(article['keywords'])
                        newsPaper['articles'].append(article)

                        for key, value in newsPaper.items():
                            print(value)
                            for contenido in value:
                                try:
                                    hoy = datetime.today()
                                    try:
                                        fecha_publicacion = ""
                                        fecha_publicacion = contenido.get("publish_date")
                                    except Exception as e:
                                        print("error", e)
                                    palabras_claves = ""
                                    if len(contenido.get("keywords")) > 0:
                                        palabras_claves = " ".join(map(str, contenido.get("keywords")))
                                    autores = ""
                                    if len(contenido.get("authors")) > 0:
                                        autores = " ".join(map(str, contenido.get("authors")))
                                    Titulo = contenido.get("title")
                                    Link = contenido.get("link")
                                    Descripcion = contenido.get("summary")
                                    texto = contenido.get("text")
                                    imagen = contenido.get("top_image")

                                    mycursor = mydb.cursor()
                                    sql = "INSERT INTO todas_las_noticias_nuevas (link,fecha_publicacion,fecha_insert,titulo,copete,texto,medio,id_provincia,imagen,autores,keywords) " \
                                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                                    val = (Link, fecha_publicacion, hoy, Titulo, Descripcion, texto,
                                           portal[0], portal[1], imagen, autores, palabras_claves)
                                    mycursor.execute(sql, val)
                                    mydb.commit()
                                    print("insert?? correctamente el link: " + portal[0] + "")
                                except Exception as e:
                                    print("error" + portal[0] + "" + str(e.msg) + "")




                #print("articles downloaded from", portal[0], " using newspaper, url: ", content.url)
            print(newsPaper)
    except Exception as e:
        print("")
