import string
import urllib
from urllib.parse import urlunsplit, urljoin, urlsplit

import feedparser
import feedparser as fp
import json

import newspaper
import requests
from bs4 import BeautifulSoup
from newspaper import Article, urls, network
from time import mktime
from datetime import datetime
import mysql.connector
from feedsearch import search
mydb = mysql.connector.connect(
  host="167.86.120.98",
  port="3307",
  database="test_portales",
  user="eze_ellena",
  password="c3hdyX8Jvnua5ZBr"
)
def findfeed(site):
    raw = requests.get(site).text
    result = []
    possible_feeds = []
    html = BeautifulSoup(raw, "html.parser")
    feed_urls = html.findAll("link", rel="alternate")
    if len(feed_urls) > 1:
        for f in feed_urls:
            t = f.get("type",None)
            if t:
                if "rss" in t or "xml" in t:
                    href = f.get("href",None)
                    if href:
                        possible_feeds.append(href)
    parsed_url = urllib.parse.urlparse(site)
    base = parsed_url.scheme+"://"+parsed_url.hostname
    atags = html.findAll("a")
    for a in atags:
        href = a.get("href",None)
        if href:
            if "xml" in href or "rss" in href or "feed" in href:
                possible_feeds.append(base+href)
    for url in list(set(possible_feeds)):
        f = feedparser.parse(url)
        if len(f.entries) > 0:
            if url not in result:
                result.append(url)
    return(result)
mycursor = mydb.cursor()
sql = "SELECT id_portal,url, id_provincia FROM portales where rss_feed is null"
mycursor.execute(sql)
sql = mycursor.fetchall()

for portal in sql:


    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 '
                             'Firefox/55.0'}
    try:
        response = requests.get(portal[1], headers=headers,timeout=10).text
    except Exception as e:
        continue
    '''
    try:
        #feed = BeautifulSoup(response, "html.parser").find("link", {"type": "application/rss+xml"})["href"]
        #feed = findfeed(portal[1])
        feed = search(portal[1])
        if len(feed) > 0:
            try:
                feed = feed[0].url
                mycursor = mydb.cursor()
                sql = "UPDATE portales set rss_feed = '"+ feed +"' where id_portal = '"+str(portal[0])+"' "
                mycursor.execute(sql)
                mydb.commit()
            except Exception as e:
                print("Insertar en la base ", e)
            print(feed)
    except Exception as e:
        continue
