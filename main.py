#! /usr/bin/env python3

#---------------------------importing libraries------------------------------#

from __future__ import unicode_literals
from bs4 import BeautifulSoup
from urllib.request import urlopen,urlretrieve,Request
import os
from urllib.error import HTTPError,URLError
import youtube_dl
import tkinter as tk
import re
import sys

#----------------------------------GUI--------------------------------------#

class songui(tk.Frame):

    def __init__(self, master):
        """creates a frame in a grid and creates widgets inside that frame"""
        f = tk.Frame(master)
        f.grid()
        self.createwidgets(f)

    def printsong(self):
        print("Song name is %s - %s"%(self.e2.get(),self.e3.get()))

    def createwidgets(self, f):
        """3 labels, 3 Entry boxes, 2 buttons.
        b1 = download button
        z
        b2 = quit button"""

        #Labels
        self.l1 = tk.Label(f, text = 'Language:')
        self.l2 = tk.Label(f, text = 'Song Name:')
        self.l3 = tk.Label(f, text = 'Singer/Movie Name:')

        #Entry box
        self.e1 = tk.Entry(f)
        self.e2 = tk.Entry(f)
        self.e3 = tk.Entry(f)
        
        #alignment in grid
        self.l1.grid(row=0, sticky='e')
        self.l2.grid(row=1, sticky='e')
        self.l3.grid(row=2, sticky='e')

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        
        #Download button
        self.b1 = tk.Button(f, text = 'Download', command = self.printsong)
        self.b1.grid(row=3, column=0)
        
        #quit button
        self.b2 = tk.Button(f, text = 'Quit', command = f.quit)
        self.b2.grid(row=3, column=1)

ui = tk.Tk()
u = songui(ui)
ui.mainloop()

#----------------------------class declaration------------------------------------#
class Songs:
    """This class refers to a mp3 file which will contain all the methods to
    download, name, singer/movie name,..etc"""

    def __init__(self, name, singer):
        """Initializes the class with name and singer/movie name in the below
        format: <singer/movie_name> - <song_name>
            ex: Linkin Park - Numb
        """
    def play(self):
        """Plays the downloaded song which is available in the music path to
        play in rhythmbox if ubuntu or windows media player if windows"""

    def saveloc(self):
        """The location in our disk where the song will be saved.
        Ubuntu: ~/Music
        Windows: C:/Music
        """

    def language(self, lang):
        """Sets the language of the song.
        Used for creating folders while saving"""

    def sites(self, lang):
        """Based on language, sites from where we could download the songs"""

#------------------------------------English Songs Scraping-----------------------------------#

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


#def musicdl(dl_url,song_name):
#    """This function takes the URL and downloads the mp3 and save it in songs
#    folder. 
#    dl_url:  the url after scraping to the correct website to find the
#    mp3.
#    p: path where song will get saved.
#    song_name: The name of the song as entered by the user.
#    """
#    p = os.path.join(os.path.expanduser('~'),'Music/songtest')
#    if not os.path.exists(p):
#        os.mkdir(p)
#    try:
#        #urlretrieve(dl_url,p+'/'+song_name)
#        req = Request(dl_url, headers={'User-Agent':'Mozilla/5.0'})
#        tmp = urlopen(req)
#        with open(p+'/'+song_name+'.mp3', 'wb') as song:
#            song.write(tmp.read())
#    except HTTPError as e:
#        print('error code', e.code)
#
#def music_frm_youtube():
#    """passes the youtube url of the song. it extracts audio alone and saves it
#    in local.
#    dl_url : youtube url for song which is priortised based on channel/views.
#    """
#    ydl_opts = {'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192',}]}
#    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#        ydl.download(['https://www.youtube.com/watch?v=gJeh_dLjPN4'])
#    print('download success')
#
#if __name__ == '__main__':
#    lang = input("Enter the language: ")
#    singer = input("Enter the author/movie name: ")
#    #dl_url ='https://www.yt-download.org/download/320-58b8d9af77ce1-10480000/mp3/PT2_F-1esPk/The%2BChainsmokers%2B-%2BCloser%2B%2528Lyric%2529%2Bft.%2BHalsey.mp3' 
#    song_name = input("Enter the song name: ")
#    if lang == "English":
#        site = ['mp3skull','beemp3','youtube']
#        music_frm_youtube()
#    elif lang == "Tamil":
#        site = ['freetamilmp3','tamilmp3world','youtube'],
#    else:
#        site = ['youtube','mp3skull']
