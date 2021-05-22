from datetime import date
import time
from urllib.parse import urlparse, urljoin
import requests
import sys
import mysql.connector
mydb = mysql.connector.connect(
  host="167.86.120.98",
  port="3307",
  database="test_portales",
  user="root",
  password="dalas.2009"
)
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
def get_all_website_links(Portal,Noticiae):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()

    internal_urls = set()
    external_urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(Portal).netloc
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0', }
    #soup = BeautifulSoup(requests.get(url,headers=headers).content, "html.parser")
    for a_tag in Noticiae.findAll("a"):
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
        #print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return internal_urls



if __name__ == "__main__":

    if len( sys.argv ) > 1:
        Id_Provincia = sys.argv[1]
    Id_Provincia = "20"
    Portales = requests.get("http://167.86.120.98:6060/Portales?id_provincia=" + Id_Provincia + "").json()

    for Portal in Portales:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                                     'Firefox/55.0'}
            response = requests.get(Portal["url"], headers=headers).text
            try:
                mycursor = mydb.cursor()
                sql = "SELECT tag FROM portales_tag where portales like " + "'%" + Portal["url"] + "%'" + ""
                mycursor.execute(sql)
                sql = mycursor.fetchall()
            except Exception as e:
                print("Error al ejecutar la consulta")
        except Exception as e:
            print("Error al ejecutar la consulta")