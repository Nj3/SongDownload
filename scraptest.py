from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,urlretrieve
import re
import youtube_dl
import sys
import os

class MyLogger(object):
    def debug(self, msg):
        pass
    
    def warning(self, msg):
        print('warning msg: ', msg)

    def error(self, msg):        
        print('error msg: ', msg)

def ytscrape(searchurl,baseurl):
    """normal scraping"""
    req = Request(searchurl, headers={'User-Agent':'Mozilla/5.0'})
    lst[:] = []
    url = urlopen(req)
    soup = BeautifulSoup(url, 'lxml')
    for i in soup.find_all('div',{'class':['yt-lockup-content','yt-lockup-meta-info']},limit=10):
        for link,views in zip(i.select('h3 > a'),i.select('ul > li')):
            if views is not None and views.next_sibling is not None:
                lst.append([baseurl+link.get('href'),views.next_sibling.text])
    for i in lst:
        i[1] = int(re.sub(r' views|,','',i[1]))
    lst.sort(key = lambda x:x[1])
    url.close()
    return lst[-1][0]

def dl_frm_youtube(yt_lnk,dlpath):
    """passes the youtube url of the song. it extracts audio alone and saves it
    in local.
    yt_lnk : youtube url for song which is priortised based on channel/views.
    """
    ydl_opts = {'format':'bestaudio/best','outtmpl':dlpath+'\\%(title)s.%(ext)s','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192',}],'logger': MyLogger()}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #ydl.download([yt_lnk])
        info = ydl.extract_info(yt_lnk, download=True)
        songname = info.get('title', None)
        #print(songname)
        if os.path.isfile(dlpath+'\\'+songname+'.mp3'):
            #print('found')
            sys.exit(0)

def beescrape(searchurl,baseurl,song,dlpath):
    """scraping in beemp3s.org"""
    req = Request(searchurl, headers={'User-Agent':'Mozilla/5.0'})
    #print('inside beescrape now')
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
                urlretrieve(link.get('href'),dlpath+'\\'+song+'.mp3')
                if os.path.isfile(dlpath+'\\'+song+'.mp3'):
                    sys.exit(0)
            innerurl.close()                    

def main():
    song = input('enter song name:')
    artist = input('enter artist name:')
    baseurl = ['https://www.youtube.com','http://beemp3s.org']
    if sys.platform == 'win32':
        dlpath = os.path.join(os.environ['USERPROFILE'],'Music','spd')
        if not os.path.exists(dlpath):
            os.mkdir(dlpath)
    else:
        dlpath = '~/Music/' + song + '.mp3'
    searchurl = [baseurl[0] + '/results?search_query=' + '+' + artist.replace(chr(32),'+') + '+' + song.replace(chr(32),'+'), baseurl[1] +'/search?query=' + artist.replace(chr(32),'+') + '+' +song.replace(chr(32),'+') + '&field=all']
    ytargs = (ytscrape(searchurl[0],baseurl[0]),dlpath)
    beeargs = (searchurl[1],baseurl[1],song,dlpath)
    args = [ytargs, beeargs]
    scrapeit = [dl_frm_youtube, beescrape]
    for func,arg in zip(scrapeit,args):
        func(*arg)


lst = []
main()

