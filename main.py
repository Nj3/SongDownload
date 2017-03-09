#! /usr/bin/env python3

#---------------------------importing libraries------------------------------#

from __future__ import unicode_literals
from bs4 import BeautifulSoup
from urllib.request import urlopen,urlretrieve,Request
import os
from urllib.error import HTTPError,URLError
import youtube_dl
import tkinter as tk

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



def musicdl(dl_url,song_name):
    """This function takes the URL and downloads the mp3 and save it in songs
    folder. 
    dl_url:  the url after scraping to the correct website to find the
    mp3.
    p: path where song will get saved.
    song_name: The name of the song as entered by the user.
    """
    p = os.path.join(os.path.expanduser('~'),'Music/songtest')
    if not os.path.exists(p):
        os.mkdir(p)
    try:
        #urlretrieve(dl_url,p+'/'+song_name)
        req = Request(dl_url, headers={'User-Agent':'Mozilla/5.0'})
        tmp = urlopen(req)
        with open(p+'/'+song_name+'.mp3', 'wb') as song:
            song.write(tmp.read())
    except HTTPError as e:
        print('error code', e.code)

def music_frm_youtube():
    """passes the youtube url of the song. it extracts audio alone and saves it
    in local.
    dl_url : youtube url for song which is priortised based on channel/views.
    """
    ydl_opts = {'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192',}]}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=gJeh_dLjPN4'])
    print('download success')

if __name__ == '__main__':
    lang = input("Enter the language: ")
    singer = input("Enter the author/movie name: ")
    #dl_url ='https://www.yt-download.org/download/320-58b8d9af77ce1-10480000/mp3/PT2_F-1esPk/The%2BChainsmokers%2B-%2BCloser%2B%2528Lyric%2529%2Bft.%2BHalsey.mp3' 
    song_name = input("Enter the song name: ")
    if lang == "English":
        site = ['mp3skull','beemp3','youtube']
        music_frm_youtube()
    elif lang == "Tamil":
        site = ['freetamilmp3','tamilmp3world','youtube'],
    else:
        site = ['youtube','mp3skull']
