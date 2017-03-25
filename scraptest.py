from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,urlretrieve
#from selenium import webdriver
import re
import youtube_dl
import sys
import os
import time

    

def ytscrape(searchurl,baseurl):
    """normal scraping"""
    req = Request(searchurl, headers={'User-Agent':'Mozilla/5.0'})
    #print(req)
    lst[:] = []
    url = urlopen(req)
    #print(url)
    soup = BeautifulSoup(url, 'lxml')
    for i in soup.find_all('div',{'class':['yt-lockup-content','yt-lockup-meta-info']},limit=10):
        for link,views in zip(i.select('h3 > a'),i.select('ul > li')):
            if views is not None and views.next_sibling is not None:
                #print(views.next_sibling.text)
                lst.append([baseurl+link.get('href'),views.next_sibling.text])
    #print(lst)
    for i in lst:
        i[1] = int(re.sub(r' views|,','',i[1]))
    #print(lst)
    lst.sort(key = lambda x:x[1])
    url.close()
    return lst[-1][0]

def dl_frm_youtube(yt_lnk):
    """passes the youtube url of the song. it extracts audio alone and saves it
    in local.
    dl_url : youtube url for song which is priortised based on channel/views.
    """
    if sys.platform == 'Windows':
        dlpath = r'C:\Downloads\%(title)s.%(ext)s'
    else:
        dlpath = r'~/Music/%(title)s.%(ext)s'
    ydl_opts = {'format':'bestaudio/best','outtmpl':dlpath,'postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192',}]}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_lnk])
    print('download success')

def beescrape(searchurl,baseurl,song):
    """scraping in beempp3s.org"""
    req = Request(searchurl, headers={'User-Agent':'Mozilla/5.0'})
    outerurl = urlopen(req)
    lst[:] = []
    outersoup = BeautifulSoup(outerurl,'lxml')
    for i in outersoup.find_all('div',{'class':'item'},limit=5):
        for link in i.select('div > a'):
            if link.get('href').startswith('http:') and re.search('remix',link.get('href'),re.IGNORECASE) is None:
                lst.append(link.get('href'))
    print(lst)
    outerurl.close()
    for i in lst:
        innerurl = urlopen(i)
        innersoup = BeautifulSoup(innerurl,'lxml')
        for link in innersoup.find_all('a',{'id':'download-button'}):
            if link.get('href').endswith('.mp3') and link.get('href').startswith('http:') and re.search('remix',link.get('href'),re.IGNORECASE) is None:
                print(link.get('href'))
                dlpath = os.path.join(os.path.expanduser('~'),'Music',song+'.mp3')
                #print(dlpath)
                urlretrieve(link.get('href'),dlpath)
                return
        innerurl.close()

def main():
    song = input('enter song name:')
    artist = input('enter artist name:')
    baseurl = ['https://www.youtube.com','http://beemp3s.org','http://mp3goo.com']
    #searchurl = baseurl + '/results?search_query=' + song.replace(chr(32),'+') + '+' + artist.replace(chr(32),'+')
    #searchurl = baseurl[1] + '/search?query=' + artist.replace(chr(32),'+') + '+' + song.replace(chr(32),'+') + '&field=all'
    searchurl = baseurl[2] + '/download/' + artist.replace(chr(32),'-') + '-' + song.replace(chr(32),'-') + '/'
    #print(searchurl)
    #dl_frm_youtube(ytscrape(searchurl,baseurl))
    #beescrape(searchurl,baseurl,song)
    #mp3gooscrape(searchurl,baseurl[2],song)


lst = []
main()

