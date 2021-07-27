import json

import mysql.connector
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import lxml

mydb = mysql.connector.connect(
    host="10.3.0.125",
    port="3307",
    database="portales",
    user="root",
    password="terminator9519"
)

while True:
    with open('data.json') as file:
        data = json.load(file)
        data = list(data)
    chrome_path = r"C:\Users\ezequ\Desktop\Santa Fe\dominicana-master\Facebook\chromedriver.exe"
    ID_GRUPO = "-505412510"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_path, chrome_options=options)
    for info in data:
        try:
            url_api = "bot1877979395:AAGlnhcH2WJp71kwzkPkpkdfl9AbSgTHbOk/sendMessage"

            persona = info["Persona"]
            # cuenta hardcodeada
            driver.implicitly_wait(30)
            driver.maximize_window()
            linkpagina = "https://www.facebook.com/ads/library/?active_status=all&ad_type=political_and_issue_ads&country=AR&view_all_page_id=" + \
                         info["Identificador_Pagina"] + ""
            driver.get(linkpagina)

            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            # sleep(3)

            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            sleep(3)

            anuncios = driver.find_elements_by_class_name("_99s5")
            # sleep(2)
            for anuncio in anuncios:
                estado_post = anuncio.find_element_by_class_name("_9cd2")
                estado_post = estado_post.text
                if estado_post == "Activo":
                    Identificador = anuncio.find_elements_by_class_name("o0aczdgd")
                    Identificador = Identificador[0].text.replace("Identificador: ", "")
                    texto_post = anuncio.find_element_by_class_name("_7jyr")
                    mycursor = mydb.cursor()
                    sql = "SELECT Identificador FROM FacebookAds where Identificador = " + str(Identificador) + ""
                    mycursor.execute(sql)
                    sql = mycursor.fetchall()
                    mydb.commit()
                    if len(sql) == 0:
                        linkNoticia = r"https://www.face" \
                                      r"book.com/ads/library/?id=" + str(Identificador)

                        mensaje = "Identificador: " + str(Identificador) + "\n\n" + "Persona: " \
                                                                               "" + persona + "\n\n" + "Estado: " + estado_post + "\n\n" \
                                  + "Post: " + texto_post.text + "\n\n" "Ver más en ->" + linkNoticia


                        try:
                            texto = texto_post.text
                            estado = estado_post
                            Identificador = str(Identificador)
                            mycursor = mydb.cursor()
                            sql = "INSERT INTO FacebookAds (Identificador,Link,persona,texto_post,estado_post) VALUES (%s,%s,%s,%s,%s) "
                            val = (Identificador, linkNoticia, persona, texto, estado)
                            mycursor.execute(sql, val)
                            mydb.commit()
                            requests.post('https://api.telegram.org/' + url_api,
                                          data={'chat_id': str(ID_GRUPO), 'text': mensaje})
                            print("insertó correctamente el link: " + linkNoticia + "")
                        except Exception as e:
                            print("error insert: " + str(e) + "")
        except Exception as e:
            print("error al ejecutar codigo " + str(e))
            continue
    driver.close()
    sleep(2)

