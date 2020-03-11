import os
import TS_Module as tools
from tkinter import filedialog
from tkinter import *

ts_folder = "/tmp/ts/"
global homedir
homedir="/home/moi/Documents/TIMOTHEE"
global src
src = None
global ref
ref = None

def tsid(json,nb):
    tsid=[]
    try:
        for i in range(nb):
            tsid.append(json['programs'][i]['program_id'])
        return tsid
    except:
        return tsid

class MPTS:
    def __init__(self,pathfile):
        self.path = pathfile
        self.name = os.path.basename(self.path)
        self.json = tools.getInfo(self.path)
        self.nb_channels = len(self.json['programs'])
        self.tsid = tsid(self.json,self.nb_channels)
        self.map = tools.mapinfo(self.json)
                    
class TS(MPTS):
    def __init__(self,name):
        self.path = ts_folder + name
        self.length = tools.get_length(self.path) # frames
        
        
class Interface(Frame):
    
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.master.title("Buttons")
        
        self.bouton_Ref = Button(self, text="Choisir Ref", fg="black", command=getRef)
        self.bouton_Ref.pack(side="right", padx=5, pady=5)
        
        self.bouton_Src = Button(self, text="Choisir Source", fg="black", command=getSrc)
        self.bouton_Src.pack(side="left", padx=5, pady=5)

        self.pack(fill=BOTH, expand=True)
        
        self.bouton_Calc = Button(self, text="Start", command=start)
        self.bouton_Calc.pack(side="bottom", padx=5, pady=5)
        self.src=None
        
    
def getRef():
    print('Importing Files')
    filename =  filedialog.askopenfilename(initialdir = homedir,title = "Select Ref file",filetypes = (("MPTS files","*.trp"),("all files","*.*")))
    ref=MPTS(filename)
    print("Name :" + ref.name)
    print("Nb channels:" + str(ref.nb_channels))
    print('Import done')
    print(ref.map)
        
def getSrc():
    print('Importing Files')
    filename =  filedialog.askopenfilename(initialdir = homedir,title = "Select Src file",filetypes = (("MPTS files","*.trp"),("all files","*.*")))
    src=MPTS(filename)
    print('Name :' + src.name)
    print("Nb channels:" + str(src.nb_channels))
    print('Import done')
    print(src.map)


def start():
    print('Extraction in progress...')
    pathout = ts_folder + ref.name
    tools.tsExtract(ref.path, pathout, ref.map[0])
    print('Extraction done')