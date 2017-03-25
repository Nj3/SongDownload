from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,urlretrieve
import re
import youtube_dl
import sys
import os
import time

    

def ytscrape(searchurl,baseurl):
    """normal scraping"""
    req = Request(searchurl, headers={'User-Agent':'Mozilla/5.0'})
    lst[:] = []
    url = urlopen(req)
    for i in soup.find_all('div',{'class':['yt-lockup-content','yt-lockup-meta-info']},limit=10):
        for link,views in zip(i.select('h3 > a'),i.select('ul > li')):
            if views is not None and views.next_sibling is not None:
                lst.append([baseurl+link.get('href'),views.next_sibling.text])
    for i in lst:
        i[1] = int(re.sub(r' views|,','',i[1]))
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
    outerurl.close()
    for i in lst:
        innerurl = urlopen(i)
        innersoup = BeautifulSoup(innerurl,'lxml')
        for link in innersoup.find_all('a',{'id':'download-button'}):
            if link.get('href').endswith('.mp3') and link.get('href').startswith('http:') and re.search('remix',link.get('href'),re.IGNORECASE) is None:
                dlpath = os.path.join(os.path.expanduser('~'),'Music',song+'.mp3')
                urlretrieve(link.get('href'),dlpath)
                return
        innerurl.close()

def main():
    song = input('enter song name:')
    artist = input('enter artist name:')
    baseurl = ['https://www.youtube.com','http://beemp3s.org']
    searchurl = [baseurl[0] + '/results?search_query=' + song.replace(chr(32),'+')
                 + '+' + artist.replace(chr(32),'+'),baseurl[1] +
                 '/search?query=' + artist.replace(chr(32),'+') + '+' +
                 song.replace(chr(32),'+') + '&field=all']
    scrapeit=[dl_frm_youtube(ytscrape(searchurl[0],baseurl[0])), beescrape(searchurl[1],baseurl[1],song)]
    for i in range(2):
        scrapeit[i]
    

lst = []
main()

