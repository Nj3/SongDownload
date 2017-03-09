#! /usr/bin/env python3
import tkinter as tk


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
