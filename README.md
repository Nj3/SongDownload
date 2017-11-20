# Overview

Download your favourite English/Tamil songs in your music folder in a simple way.

## Pre-requisites:

1. For Ubuntu, Python 3.5+. For windows, Use either python 3.5+ or use as a standalone application.
2. youtube-dl - if not available install it using `pip install youtube-dl`
3. google - if not available install it using `pip install google`

## Usage:

### Ubuntu:

Downloaded songs will be available in the path: `~/Music/SD/`

Run `python3 <Script path>` in the terminal after downloading the main.py file. After that follow below mentioned steps on how to use GUI.

### Windows:

#### Commandline:

If you want to use in CMD, run `python <script path>` after downloading the main.py file. After that follow below mentioned steps on how to use GUI.

#### Standalone application:

If you don't have python installed, download the .rar file. then do the following steps.
1. Extract it a folder.
2. Navigate it to dist -> main -> main.exe and Run it.

After that follow below mentioned steps on how to use GUI.

### How to use GUI:

Once you followed the steps given above, you will get a windows like below:
[![SD_1.png](https://s7.postimg.org/tbn8ax7ln/SD_1.png)](https://postimg.org/image/9tskuzanr/)

1. Choose either English/Tamil.
2. Enter the song name and artist/movie name in text box as shown below. Click Download.

[![SD_2.png](https://s7.postimg.org/5xf8z2hzf/SD_2.png)](https://postimg.org/image/sm4fymzd3/)

3. After the song is downloaded, you will see a dialog box showing download is completed like below:

[![SD_3.png](https://s7.postimg.org/w5qdohk3f/SD_3.png)](https://postimg.org/image/45ma47gmv/)

4. you can continue downloading songs by entering song name and artist name in text box. Once you are done. close the window and console closes automatically.

## Known Issues:

when we switch the language from Tamil to english after downloading atleast one song, it switches perfectly and works as expected. When we switch from English to Tamil, it doesn't work correctly.
As a workaround, please reopen the application when you want to switch the language.