#! /usr/bin/env python3

#---------------------------importing libraries------------------------------#

from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve, Request
import os
from urllib.error import HTTPError, URLError
import youtube_dl
import tkinter as tk
import re
import sys
import google
from selenium import webdriver

#----------------------------------GUI--------------------------------------#

class SongUI(tk.Frame): #pylint: disable=too-many-ancestors
    """Builds Front end to get user input and download"""
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        master.minsize(width=500, height=500)
        self.master = master
        self.master.title('Song Downloader')

        #create 2 frames
        outerframe = tk.Frame(width=500, height=500)
        centerframe = tk.Frame(width=300, height=300)
        outerframe.grid(sticky=tk.N+tk.E+tk.S+tk.W)
        centerframe.place(in_=outerframe, anchor='c', relx=.5, rely=.5)

        #initialize widgets
        self.initialize(centerframe)
        
    def initialize(self, f):
        """1 drop down for language selection.
        based on selection, create 2 types of widgets;1 for english, 1 for tamil.
        Download button to start the song download.
        Labels wherever required."""

        def usr_selection(value):
            """This function will get triggered after user select a value in drop down.
            Based on this value, it will create widgets"""
            print(value)
            #song row 
            self.lbl_song.grid(row=1, column=0, sticky=tk.E, pady=(20, 0))
            self.entry_song.grid(row=1, column=1, columnspan=2, pady=(20, 0))
            if value == 'English':
                #singer row
                self.lbl_artist.grid(row=2, column=0, sticky=tk.E)
                self.entry_artist.grid(row=2, column=1, columnspan=2)
            else:
                #singer row
                self.lbl_movie.grid(row=2, column=0, sticky=tk.E)
                self.entry_movie.grid(row=2, column=1, columnspan=2)
            
            #download button alignment after everything is created
            self.button_dl.grid(row=3, column=0, pady=(30, 0), columnspan=3)
        
        #required labels
        self.lbl_lang = tk.Label(f, text='Language:')
        self.lbl_song = tk.Label(f, text='Enter the Song Name:')
        self.lbl_movie = tk.Label(f, text='Enter the Movie Name:')
        self.lbl_artist = tk.Label(f, text='Enter the Singer Name:')

        #Entry boxes
        self.entry_song = tk.Entry(f)
        self.entry_movie = tk.Entry(f)
        self.entry_artist = tk.Entry(f)

        #Language dropdown
        self.langvar = tk.StringVar()
        self.langvar.set('Select Language')
        self.dd_lang = tk.OptionMenu(f, self.langvar, 'English', 'Tamil', command=usr_selection)
        
        #download button
        self.button_dl = tk.Button(f, text='Download', command=self.printsong)

        #alignment in centerframe in grid format
        self.lbl_lang.grid(row=0, column=0, sticky=tk.E)
        self.dd_lang.grid(row=0, column=1)
        
    def printsong(self):
        print('GUI working successfully')
        print(self.entry_song.get(), self.entry_movie.get(), self.entry_artist.get())


root = tk.Tk()
root.resizable(width=False, height=False)
app = SongUI(master=root)
app.mainloop()

#----------------------------class declaration------------------------------------#
class Songs:
    """This class refers to a mp3 file which will contain all the methods to
    download, name, singer/movie name,..etc"""

    def __init__(self, name, singer):
        """Initializes the class with name and singer/movie name in the below
        format: <singer/movie_name> - <song_name>
            ex: Linkin Park - Numb
        """
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

#----------------------------------------------Tamil songs------------------------------------------------#

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
