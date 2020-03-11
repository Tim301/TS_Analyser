#!/usr/bin/env python3

__name='__main__'

#def main():
#    pass
#
#if __name__ = '__main'__:
#    main()

import os
from tkinter import *
from TS_Class import *

def ask_quit():
    root.destroy()

#Initialisation
print('Initialisation')
ts_folder = "/tmp/ts/"
if not(os.path.isdir(ts_folder)):
    os.makedirs(ts_folder)

root = Tk()
root.geometry("600x200+300+300")
app = Interface()
root.protocol("WM_DELETE_WINDOW", ask_quit)
root.mainloop()