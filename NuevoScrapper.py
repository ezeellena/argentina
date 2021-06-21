import feedparser as fp
import json
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
mydbEze = mysql.connector.connect(
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
                print(category)
                try:
                    newsPaper["category"].append(category)
                except Exception as e:
                    print("")
            for feed_url in paper.feed_urls():
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

                try:
                    article['summary'] = a.summary
                except Exception as e:
                    print("")
                try:
                    article['keywords'] = a.keywords
                except Exception as e:
                    print("")

                newsPaper['articles'].append(article)

                #print("articles downloaded from", portal[0], " using newspaper, url: ", content.url)
            print(newsPaper)
    except Exception as e:
        print("")
