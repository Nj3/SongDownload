#! /usr/bin/env python3
import tkinter as tk

ui = tk.Tk()
lbl = tk.Label(ui, text = 'Hello, can you hear me?')
lbl.grid(row = 0, column = 0)

ent1 = tk.Entry()
ent1.grid(row = 0, column = 1)

print(ent1.get())

ui.mainloop()
