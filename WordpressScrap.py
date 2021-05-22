import base64
import json
from datetime import datetime

import requests
import mysql.connector
from bs4 import BeautifulSoup
import urllib.request
"""
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Server=localhost;'
                      'Database=ScraperNoticias;'
                      'Trusted_Connection=yes;')
"""
conn = mysql.connector.connect(
  host="167.86.120.98",
  port="3307",
  database="test_portales",
  user="root",
  password="dalas.2009"
)

def obtenerTitulo(response):
    Titulo = ""
    try:
        Titulo = BeautifulSoup(response, "html.parser").find("meta", {"name": "twitter:title"})["content"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = BeautifulSoup(response, "html.parser").find("meta", {"property":"og:title"})["content"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[0]["headline"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Titulo = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)["headline"]
        return Titulo
    except Exception as e:
        print("No se pudo obtener el Título ", e)
def obtenerDescripcion(response):
    Descripcion = ""
    try:
        Descripcion = BeautifulSoup(response, "html.parser").find("meta", {"name":"twitter:description"})["content"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Descripcion = BeautifulSoup(response, "html.parser").find("meta", {"property":"og:description"})["content"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Descripcion = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)[0]["description"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener el Título ", e)
    try:
        Descripcion = json.loads(BeautifulSoup(response, "html.parser").find("script", {"type": 'application/ld+json'}).string)["description"]
        return Descripcion
    except Exception as e:
        print("No se pudo obtener el Título ", e)
def obtenerImagen(response):
    Imagen = ""
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


if __name__ == "__main__":
    try:
        while True:
            try:
                sql = "SElECT id_padre as idpadre FROM publicador group by id_padre"
                mycursor = conn.cursor()
                mycursor.execute(sql)
                PublicadoresAgrupados = mycursor.fetchall()

                for publiAgrupado in PublicadoresAgrupados:

                    Provincias = []
                    sql = "SElECT id_destino FROM publicador where id_padre =" + str(publiAgrupado[0]) + " group by id_destino"
                    mycursor = conn.cursor()
                    mycursor.execute(sql)
                    destinoAgrupado = mycursor.fetchall()
                    # if destinoAgrupado == 1:
                    sql = "SElECT id_provincia FROM publicador where id_padre ="+str(publiAgrupado[0])+" group by id_provincia"
                    mycursor = conn.cursor()
                    mycursor.execute(sql)
                    provinciasAgrupadas = mycursor.fetchall()

                    for pronvicia in provinciasAgrupadas:
                        Provincias.append(pronvicia[0])
                    prov = ','.join(str(e) for e in Provincias)
                    sql = "SElECT tema FROM publicador where id_padre =" + str(publiAgrupado[0]) + " group by tema"
                    mycursor = conn.cursor()
                    mycursor.execute(sql)
                    temasAgrupados = mycursor.fetchall()
                    temasAgrupados = ["lluvias"]
                    for tema in temasAgrupados:
                        try:
                            #if publiAgrupado[0] == "http://stg.kernelinformatica.com.ar/~wp001":
                            sql = "SELECT link FROM todas_las_noticias where medio in " \
                                  "(select link from portales_wordpress)" \
                                     "and link not in " \
                                     "(select link from noticias_basura) " \
                                     "and link not in " \
                                     "(select link from noticias_enviadas_wordpress)" \
                                     "and texto like " + '"%' + \
                                  tema[0] + '%"'
                            mycursor = conn.cursor()
                            mycursor.execute(sql)
                            Portales = mycursor.fetchall()
                        except Exception as e:
                            print("Error al Obtener portales ", e)
                        for link in Portales:
                            try:
                                response = requests.get(link[0]).text
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

                                try:
                                    user = 'admin-wp001'
                                    pythonapp = 'O3nN NejK qSiV MDHR xO4I Cplp'
                                    url = 'http://stg.kernelinformatica.com.ar/~wp001/wp-json/wp/v2'
                                    data_string = user + ':' + pythonapp
                                    token = base64.b64encode(data_string.encode())
                                    headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
                                    imgsrc = Imagen
                                    post = {'date': str(datetime.today()),
                                            'title': Titulo,
                                            'slug': 'rest-api-1',
                                            'status': 'publish',
                                            'content': '<img src='
                                                       + imgsrc
                                                       + '>' + Descripcion,
                                            'author': '1',
                                            'excerpt': 'Exceptional post!',
                                            'format': 'standard',
                                            'post_tag': ['Campo', 'Siembra'],
                                            'category': ['Actualidad']
                                            }
                                    r = requests.post(url + '/posts', headers=headers, json=post)

                                    print('Your post is published on ' + json.loads(r.content.decode('utf-8'))['link'])
                                except Exception as e:
                                    print("Error al Obtener portales ", e)
                            except Exception as e:
                                print("Error al Obtener portales ", e)


            except Exception as e:
                print("Error al Obtener portales ", e)
    except Exception as e:
        print("Error al Obtener portales ", e)