#! /usr/bin/env python3

#---------------------------importing libraries------------------------------#
import os
import tkinter as tk
import sys
import urllib.parse
from urllib.request import urlopen, urlretrieve, Request
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
import youtube_dl
import re
import google
from selenium import webdriver

#----------------------------class declaration------------------------------------#
class Songs(object):
    """This class refers to a mp3 file which will contain all the methods to
    download, name, singer/movie name,..etc"""

    def __init__(self, lang, song_nm, movie_name=None, artist_name=None):
        """Initializes the class with name and singer/movie name in the below
        format: <singer/movie_name> - <song_name>
            ex: Linkin Park - Numb
        """
        if lang == 'English':
            self.lang = lang
            self.song_nm = song_nm
            self.singer = artist_name
        else:
            self.lang = lang
            self.song_nm = song_nm
            self.singer = movie_name
        self.dlpath = None
        self.saveloc()
        self.dl_sites = []
        self.url_list = []
        self.searchurl = []
        #self.sites()

    def __repr__(self):
        """prints out the string representation of song object"""
        return 'The song name is %r from %r'%(self.song_nm, self.singer)

    def saveloc(self):
        """The location in our disk where the song will be saved.
        Ubuntu: ~/Music/SD/<lang>/singer/*
        Windows: C:/Music/SD/<lang>/singer/*
        """
        if sys.platform == 'win32':
            dlpath = os.path.join(os.environ['USERPROFILE'], 'Music', 'SD', self.lang, self.singer)
            if not os.path.exists(dlpath):
                os.mkdir(dlpath)
        else:
            dlpath = os.path.join(os.path.expanduser('~'), 'Music', 'SD', self.lang, self.singer)
            if not os.path.exists(dlpath):
                os.mkdir(dlpath)
        self.dlpath = dlpath
        return
#------------------------------------English Songs Scraping-----------------------------------#

    def ytscrape(self):
        """searchurl will contain the url when we search in youtube. Based on that url, scraping will be done.
        Best selection will be done based on number of views."""
        req = Request(self.searchurl[0], headers={'User-Agent':'Mozilla/5.0'})
        self.url_list[:] = []
        url = urlopen(req)
        soup = BeautifulSoup(url, 'lxml')
        for i in soup.find_all('div', {'class':['yt-lockup-content','yt-lockup-meta-info']}, limit=10):
            for link, views in zip(i.select('h3 > a'), i.select('ul > li')):
                if views is not None and views.next_sibling is not None:
                    self.url_list.append([self.dl_sites[0] + link.get('href'), views.next_sibling.text])
        for i in self.url_list:
            i[1] = int(re.sub(r' views|,', '', i[1]))
        self.url_list.sort(key=lambda x: x[1])
        url.close()
        return self.url_list[-1][0]

    def dl_frm_youtube(self, yt_lnk):
        """passes the youtube url of the song. it extracts audio alone and saves it
        in local.
        yt_lnk : youtube url for song which is priortised based on channel/views.
        """
        ydl_opts = {'format':'bestaudio/best','outtmpl':self.dlpath+'\\%(title)s.%(ext)s','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192',}]}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #ydl.download([yt_lnk])
            info = ydl.extract_info(yt_lnk, download=True)
            songname = info.get('title', None)
            #print(songname)
            if os.path.isfile(self.dlpath+'\\'+songname+'.mp3'):
                #print('found')
                return True

    def beescrape(self):
        """scraping in beemp3s.org"""
        req = Request(self.searchurl[1], headers={'User-Agent':'Mozilla/5.0'})
        #print('inside beescrape now')
        outerurl = urlopen(req)
        self.url_list[:] = []
        outersoup = BeautifulSoup(outerurl, 'lxml')
        for i in outersoup.find_all('div', {'class':'item'}, limit=5):
            for link in i.select('div > a'):
                if link.get('href').startswith('http:') and re.search('remix', link.get('href'), re.IGNORECASE) is None:
                    self.url_list.append(link.get('href'))
        outerurl.close()
        for i in self.url_list:
            innerurl = urlopen(i)
            innersoup = BeautifulSoup(innerurl, 'lxml')
            for link in innersoup.find_all('a', {'id':'download-button'}):
                if link.get('href').endswith('.mp3') and link.get('href').startswith('http:') and re.search('remix', link.get('href'), re.IGNORECASE) is None:
                    urlretrieve(link.get('href'), self.dlpath+'\\'+ self.song_nm + '.mp3')
                    if os.path.isfile(self.dlpath + '\\' + self.song_nm + '.mp3'):
                        return True
                innerurl.close()

#----------------------------------------------Tamil songs------------------------------------------------#

    def tamildl(self):
        """custom search in google using `site:freetamilmp3.in` trick"""
        baseurl = 'http://freetamilmp3.in/'
        self.url_list[:] = []
        for url in google.search(self.searchurl[0], tld='co.in', lang='eng', start=0, stop=5):
            self.url_list.append(url)
        for url in self.url_list:
            driver = webdriver.PhantomJS()
            driver.get(url)
            urlsrc = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(urlsrc, 'lxml')
            for link in soup.find_all('a'):
                if re.search('Full mp3', link.text, re.IGNORECASE) is not None:
                    if link.get('href').startswith('http:'):
                        dllink = link.get('href')
                    else:
                        dllink = urllib.parse.urljoin(baseurl, link.get('href'))
                    #req = requests.get(dllink)
                    urlretrieve(urllib.parse.quote(dllink,safe='/|:'), os.path.join(self.dlpath, self.song_nm + '.mp3'))
                    if os.path.isfile(os.path.join(self.dlpath, self.song_nm + '.mp3')):
                        return True

    def ytscrape_tamil(self):
        """searchurl will contain the url when we search in youtube. Based on that url, scraping will be done.
        Best selection will be done based on number of views."""
        req = Request(self.searchurl[1], headers={'User-Agent':'Mozilla/5.0'})
        self.url_list[:] = []
        url = urlopen(req)
        soup = BeautifulSoup(url, 'lxml')
        for i in soup.find_all('div', {'class':['yt-lockup-content','yt-lockup-meta-info']}, limit=10):
            for link, views in zip(i.select('h3 > a'), i.select('ul > li')):
                if views is not None and views.next_sibling is not None:
                    self.url_list.append([self.dl_sites[1] + link.get('href'), views.next_sibling.text])
        for i in self.url_list:
            i[1] = int(re.sub(r' views|,', '', i[1]))
        self.url_list.sort(key=lambda x: x[1])
        url.close()
        return self.url_list[-1][0]

    def dl_frm_youtube_tamil(self, yt_lnk):
        """passes the youtube url of the song. it extracts audio alone and saves it
        in local.
        yt_lnk : youtube url for song which is priortised based on channel/views.
        """
        ydl_opts = {'format':'bestaudio/best','outtmpl':self.dlpath+'\\%(title)s.%(ext)s','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192',}]}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #ydl.download([yt_lnk])
            info = ydl.extract_info(yt_lnk, download=True)
            songname = info.get('title', None)
            #print(songname)
            if os.path.isfile(self.dlpath+'\\'+songname+'.mp3'):
                #print('found')
                return True

    def sites(self):
        """Based on language, sites from where we could download the songs.
        Tamil: freetamilmp3.in, youtube
        English:youtube, beemp3s.org"""
        if self.lang == 'English':
            self.dl_sites = ['https://www.youtube.com', 'http://beemp3s.org']
            self.searchurl = [self.dl_sites[0] + '/results?search_query=' + '+' + self.singer.replace(chr(32),'+') + '+' + self.song_nm.replace(chr(32),'+'), self.dl_sites[1] +'/search?query=' + self.singer.replace(chr(32),'+') + '+' + self.song_nm.replace(chr(32),'+') + '&field=all']
            scrapeit = [self.dl_frm_youtube(self.ytscrape()), self.beescrape()]
            for fn in scrapeit:
                flag = fn()
                if flag:
                    print('song downloaded successfully')
                    break
        else:
            self.dl_sites = ['http://freetamilmp3.in/', 'https://www.youtube.com']
            self.searchurl = ['site:freetamilmp3.in' + self.singer + self.song_nm, self.dl_sites[1] + '/results?search_query=' + '+' + self.singer.replace(chr(32),'+') + '+' + self.song_nm.replace(chr(32),'+')]
            #call tamil songs scrape
            scrapeit = [self.tamildl(), self.dl_frm_youtube_tamil(self.ytscrape_tamil())]
            for fn in scrapeit:
                flag = fn()
                if flag:
                    print('song downloaded successfully')
                    break
        return


def main(lang, song, mov, artist):
    """this function is the main controller for calling different function"""
    print('successfully called main fn %s,%s,%s,%s'%(lang, song, mov, artist))
    if lang == 'English':
        song_Args = [lang, song, None, artist]
    else:
        song_Args = [lang, song, mov, None]
    mp3_song = Songs(*song_Args)
    mp3_song.sites()


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
            #set language back to variable so that we can use it later.
            self.langvar.set(value)
            
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
        """Just to check whether all variables are set correctly and call the main fn to start download"""
        print('GUI working successfully')
        print(self.entry_song.get(), self.entry_movie.get(), self.entry_artist.get())
        main(self.langvar.get(),self.entry_song.get(), self.entry_movie.get(), self.entry_artist.get())

root = tk.Tk()
root.resizable(width=False, height=False)
app = SongUI(master=root)
app.mainloop()

