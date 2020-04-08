import os
from tkinter import filedialog
from tkinter import *
from MPTS import MPTS
import TS_Module as tools
from TS_Matchtemplate import gap_finder

ts_folder = "/tmp/ts/"

global homedir
homedir="/home/moi/Documents/TIMOTHEE"

class Interface(Frame):
    
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.master.title("Buttons")
        
        self.bouton_Ref = Button(self, text="Choisir Ref", fg="black", command=self.getRef)
        self.bouton_Ref.pack(side="right", padx=5, pady=5)
        
        self.bouton_Src = Button(self, text="Choisir Source", fg="black", command=self.getSrc)
        self.bouton_Src.pack(side="left", padx=5, pady=5)

        self.pack(fill=BOTH, expand=True)
        
        self.bouton_Calc = Button(self, text="Start", command=self.start)
        self.bouton_Calc.pack(side="bottom", padx=5, pady=5)
        self.src=None
        self.ref=None
        
    
    def getRef(self):
        print('Importing Files')
        filename =  filedialog.askopenfilename(initialdir = homedir,title = "Select Ref file",filetypes = (("MPTS files","*.trp"),("all files","*.*")))
        self.ref=MPTS(filename)
        print("Name :" + self.ref.name)
        print("Nb channels:" + str(self.ref.nb_channels))
        print('Import done')
        print(self.ref.map)
        
    def getSrc(self):
        print('Importing Files')
        filename =  filedialog.askopenfilename(initialdir = homedir,title = "Select Src file",filetypes = (("MPTS files","*.trp"),("all files","*.*")))
        self.src=MPTS(filename)
        print('Name :' + self.src.name)
        print("Nb channels:" + str(self.src.nb_channels))
        print('Import done')
        print(self.src.map)

    def start(self):
        print('Extraction in Ref progress...')
        pathoutref = ts_folder + self.ref.name[:-3] + "ts"
        tools.tsExtract(self.ref.path, pathoutref, self.ref.map[0])
        print('Extraction Ref done')
        print('Extraction in Src progress...')
        pathoutsrc = ts_folder + self.src.name[:-3] + "ts"
        tools.tsExtract(self.src.path, pathoutsrc, self.src.map[0])
        print('Extraction Src done')
        print('Research delay')
        #research similiraty in a window of 5s
        gap_finder(pathoutref, pathoutsrc, 5)
        print('Research done')
        
        