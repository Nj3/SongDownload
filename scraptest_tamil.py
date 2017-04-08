from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os
import re
import sys
import google
from selenium import webdriver
import urllib.parse


def tamildl(searchquery, dlpath, song):
    """custom search in google using `site:freetamilmp3.in` trick"""
    baseurl = 'http://freetamilmp3.in/'
    lst[:] = []
    for url in google.search(searchquery, tld='co.in',lang='eng',start = 0, stop = 5):
        lst.append(url)
    for url in lst:
        driver = webdriver.PhantomJS()
        driver.get(url)
        urlsrc = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(urlsrc, 'lxml')
        for link in soup.find_all('a'):
            if re.search('Full mp3',link.text,re.IGNORECASE) is not None:
                if link.get('href').startswith('http:'):
                    dllink = link.get('href')
                else:
                    dllink = urllib.parse.urljoin(baseurl,link.get('href'))
                req = requests.get(dllink)
                urlretrieve(urllib.parse.quote(dllink,safe='/|:'), os.path.join(dlpath,song+'.mp3'))
                if os.path.isfile(os.path.join(dlpath,song+'.mp3')):
                    sys.exit(0)

def main():
    song = input('enter the song name:')
    movie = input('enter the movie name:')
    if sys.platform == 'win32':
        dlpath = os.path.join(os.environ['USERPROFILE'],'Music','spd')
        if not os.path.exists(dlpath):
            os.mkdir(dlpath)
    else:
        dlpath = '~/Music/' + song + '.mp3'
    tamildl(searchquery,dlpath,song)

lst = []
main()
