#! /usr/bin/env python3
import tkinter as tk

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
