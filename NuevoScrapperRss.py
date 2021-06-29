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
  host="167.86.120.98",
  port="3307",
  database="test_portales",
  user="eze_ellena",
  password="c3hdyX8Jvnua5ZBr"
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
        sql = "SELECT url, id_provincia,rss_feed FROM portales where rss_feed is not null"
        mycursor.execute(sql)
        sql = mycursor.fetchall()
        for portal in sql:
            try:
                d = fp.parse(portal[2])
                newsPaper = {
                    "articles": []
                }
            except Exception as e:
                print("Error al obtener RSS",e)
            lista = []
            if len(d.entries) == 0:
                print("No se obtuvieron articulos", portal[2])
            if len(d.entries) > 0:
                for url in d.entries:
                    lista.append(url.link)

                format_strings = ','.join(['%s'] * len(d.entries))
                medio = portal[0]
                mycursor = mydb.cursor()
                sqlnot = "SELECT *  FROM todas_las_noticias_rss WHERE medio like '%"+medio+"%' and link IN ("+format_strings+")"
                val = lista
                mycursor.execute(sqlnot, val)
                sqlnot = mycursor.fetchall()
                for remove in sqlnot:
                    lista.remove(remove[0])
                if len(lista) > 0:
                    for link in lista:
                        # Check if publish date is provided, if no the article is skipped.
                        # This is done to keep consistency in the data and to keep the script from crashing.

                        article = {}


                        try:
                            content = Article(link)
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
                        article['link'] = link

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
                            article['published'] = content.publish_date
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
                            article['summary'] = content.summary
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

                    for key, value in newsPaper.items():
                        for contenido in value:
                            try:
                                hoy = datetime.today()
                                try:
                                    fecha_publicacion = ""
                                    fecha_publicacion = contenido.get("published")
                                except Exception as e:
                                    print("error", e)
                                palabras_claves = ""
                                if len(contenido.get("keywords")) > 0:
                                    palabras_claves = " ".join(map(str,contenido.get("keywords")))
                                autores = ""
                                if len(contenido.get("authors")) > 0:
                                    autores = " ".join(map(str,contenido.get("authors")))
                                Titulo = contenido.get("title")
                                Link = contenido.get("link")
                                Descripcion = contenido.get("summary")
                                texto = contenido.get("text")
                                imagen = contenido.get("top_image")

                                mycursor = mydb.cursor()
                                sql = "INSERT INTO todas_las_noticias_rss (link,fecha_publicacion,fecha_insert,titulo,copete,texto,medio,id_provincia,medio_rss,imagen,autores,keywords) " \
                                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                                val = (Link, fecha_publicacion,hoy, Titulo, Descripcion, texto,
                                       portal[0], portal[1], portal[2],imagen,autores,palabras_claves)
                                mycursor.execute(sql, val)
                                mydb.commit()
                                print("insertó correctamente el link: " + Link + "")
                            except Exception as e:
                                print("error" + Link + "" + str(e.msg) + "")
                        """
                        try:
                            mycursor = mydb.cursor()
                            sql = "SELECT url, id_provincia FROM portales where id_provincia = '20'"
                            mycursor.execute(sql)
                            sql = mycursor.fetchall()
                        except Exception as e:
                            print("Insertar en la base ", e)
                        """
        """
        mycursor = mydb.cursor()
        sql = "SELECT url, id_provincia FROM portales where id_provincia = '20'"
        mycursor.execute(sql)
        sql = mycursor.fetchall()

        for portal in sql:
            print("Building site for ", portal[0])
            paper = newspaper.build(portal[0], memoize_articles=False)
            article = {}
            newsPaper = {
                "link": portal[0],
                "category": [],
                "feed": [],
                "articles": []
            }
            noneTypeCount = 0

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
                a = Article(content.url, keep_article_html=True)
                a.download()
                a.parse()

                response = requests.get(content.url, headers=headers).text

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
                        article['publish_date'] = content.publish_date.isoformat()
                    elif a.publish_date is not None or not "":
                        article['publish_date'] = a.publish_date.isoformat()
                    else:
                        article['publish_date'] = obtenerFechaPublicacion(response)
                except Exception as e:
                    try:
                        article['publish_date'] = a.publish_date.isoformat()
                    except Exception as e:
                        article['publish_date'] = obtenerFechaPublicacion(response)
                print(article['publish_date'])

                try:
                    if content.top_image is not None or not "":
                        article['top_image'] = content.top_image
                    elif a.top_image is not None or not "":
                        article['top_image'] = a.top_image
                    else:
                        article['top_image'] = obtenerFechaPublicacion(content.url)
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

                for item in newsPaper.items():
                    try:
                        mycursor = mydb.cursor()
                        sql = "SELECT url, id_provincia FROM portales where id_provincia = '20'"
                        mycursor.execute(sql)
                        sql = mycursor.fetchall()
                    except Exception as e:
                        print("Insertar en la base ",e)

        """


                #print("articles downloaded from", portal[0], " using newspaper, url: ", content.url)

    except Exception as e:
        print("")
