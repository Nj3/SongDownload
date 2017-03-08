#---------------------------importing libraries------------------------------#
from __future__ import unicode_literals
from bs4 import BeautifulSoup
from urllib.request import urlopen,urlretrieve,Request
import os
from urllib.error import HTTPError,URLError
import youtube_dl

#----------------------------class declaration------------------------------------#
class Songs(object):
    """This class refers to a mp3 file which will contain all the methods to
    download, name, singer/movie name,..etc"""

    def __init__(self, name, singer):
        """Initializes the class with name and singer/movie name in the below
        format: <singer/movie_name> - <song_name>
            ex: Linkin Park - Numb
        """



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
