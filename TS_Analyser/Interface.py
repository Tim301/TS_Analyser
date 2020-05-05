import os
import time
import numpy
from tkinter import filedialog
from tkinter import *
from MPTS import MPTS
import TS_Module as tools
from TS_Matchtemplate import gap_finder
from TS_Quality import Quality
import matplotlib
import matplotlib.pyplot as plt
import statistics
from bitrate import getBitrate
import csv
import cv2

ts_folder = "/tmp/ts/"

global homedir
homedir = "/home/moi/PycharmProjects/Plotbitrate"


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

        self.bouton_Src2 = Button(self, text="Choisir Source", fg="black", command=self.getSrc2)
        self.bouton_Src2.pack(side="left", padx=5, pady=5)

        self.pack(fill=BOTH, expand=True)

        self.bouton_Calc = Button(self, text="Start", command=self.start)
        self.bouton_Calc.pack(side="bottom", padx=5, pady=5)
        self.src = None
        self.ref = None

    def getRef(self):
        print('Importing Files')
        filename = filedialog.askopenfilename(initialdir=homedir, title="Select Ref file",
                                              filetypes=(("MPTS files", "*.trp"), ("all files", "*.*")))
        self.ref = MPTS(filename)
        print("Name :" + self.ref.name)
        print("Nb channels:" + str(self.ref.nb_channels))
        print('Import done')
        print(self.ref.map)

    def getSrc(self):
        print('Importing Files')
        filename = filedialog.askopenfilename(initialdir=homedir, title="Select Src file",
                                              filetypes=(("MPTS files", "*.trp"), ("all files", "*.*")))
        self.src = MPTS(filename)
        print('Name :' + self.src.name)
        print("Nb channels:" + str(self.src.nb_channels))
        print('Import done')
        print(self.src.map)

    def getSrc2(self):
        print('Importing Files')
        filename = filedialog.askopenfilename(initialdir=homedir, title="Select Src file",
                                              filetypes=(("MPTS files", "*.trp"), ("all files", "*.*")))
        self.src2 = MPTS(filename)
        print('Name :' + self.src2.name)
        print("Nb channels:" + str(self.src2.nb_channels))
        print('Import done')
        print(self.src2.map)

    def start(self):
        choose = 0
        methode = ["PSNR","Py_PSNR","SSIM","VMAF"]
        print(methode[choose])
        start = time.time()
        EyeQ = [0,1,2,3,4,5,6]
        Prod = [7,8,9,10,11,12,13]
        Ref = 14
        OUTPUTBASENAME ="Test"
        x = 2
        while x<7:
            OUTPUTFILENAME= OUTPUTBASENAME + "_Profile" + str(x+1)
            index_ref = None
            index_src = None
            index_ref2= None
            index_src2= None
            start= time.time()
            print('Extraction in Ref progress...')
            refname = "Reference_20Mbps.ts"
            pathoutref = ts_folder + refname
            print(self.ref.path)
            print(pathoutref)
            tools.tsExtract(self.ref.path, pathoutref, self.ref.map[Ref])
            print('Extraction Ref done')
            print('Extraction in Src progress...')
            srcname = "EyeQ_profile"+str(x+1) + ".ts"
            pathoutsrc = ts_folder + "EyeQ_profile"+str(x+1) + ".ts"
            tools.tsExtract(self.src.path, pathoutsrc, self.src.map[EyeQ[x]])
            print('Extraction in Src progress...')
            srcname2 = "Prod_profile" + str(x+1) + ".ts"
            pathoutsrc2 = ts_folder + "Prod_profile"+str(x+1) + ".ts"
            tools.tsExtract(self.src2.path, pathoutsrc2, self.src.map[Prod[x]])
            print('Extraction Src done')

            print('Research delay')
            # research similarity in a window of 5s

            length = tools.get_minlength(pathoutsrc,pathoutsrc2,pathoutref)

            index_ref, index_src = gap_finder(pathoutref, refname, pathoutsrc, srcname, 5, True)
            index_ref2, index_src2 = gap_finder(pathoutref, refname, pathoutsrc2, srcname2, 5, True)
            print('Research done')
            print('Matching results ref[]:')
            print(index_ref)
            print('Matching results src[]:')
            print(index_src)
            print('Matching results ref2[]:')
            print(index_ref2)
            print('Matching results src2[]:')
            print(index_src2)

            Score , frame, bitrate_src= Quality(pathoutref, index_ref, pathoutsrc, index_src, length, methode[choose])

            with open(srcname +'.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Frame",methode[choose], "Bitrate"])
                i = 0
                while (i < len(Score)):
                    writer.writerow([i,str(Score[i]).replace('.',','), str(bitrate_src[i]).replace('.',',')])
                    i = i + 1
                if methode[choose] == "PSNR":
                    writer.writerow(["","Mean PSNR (dB)", "Mean bitrate (Kb/s)"])
                if methode[choose] == "PY_PSNR":
                    writer.writerow(["","Mean PSNR (dB)", "Mean bitrate (Kb/s)"])
                if methode[choose] == "SSIM":
                    writer.writerow(["","Mean SSIM", "Mean bitrate (Kb/s)"])
                if methode[choose] == "VMAF":
                    writer.writerow(["","Mean VMAF", "Mean bitrate (Kb/s)"])
                writer.writerow(["","=MOYENNE(B2:B"+str(i+1)+")", "=MOYENNE(C2:C"+str(i+1)+")"])

            t=[]
            for i in range(frame):
                t.append(i)
            print(len(t))
            fig, ax = plt.subplots()
            ax.set(title=srcname)
            ax.set_xlabel("Frame")
            if methode[choose] == "PSNR" or methode[choose] == "Py_PSNR":
                ax.set_ylabel('PSNR (dB)', color="tab:blue")
            if methode[choose] == "SSIM":
                ax.set_ylabel('SSIM', color="tab:blue")
            if methode[choose] == "VMAF":
                ax.set_ylabel('VMAF', color="tab:blue")
            ax.plot(t, Score, color="tab:blue")
            ax.tick_params(axis='y', color="tab:blue")

            ax2 = ax.twinx()
            ax2.set_ylabel('Bitrate (Kbit/s)', color="tab:red")
            ax2.plot(t, bitrate_src,label='Bitrate',color = "tab:red")
            ax2.tick_params(axis='y', color="tab:red")

            Efficacite = str(numpy.mean(Score))
            Efficacite = "Mean Score : " + Efficacite[:7] + " (dB)"
            ax2.text(0.95, 0.92, Efficacite,verticalalignment='bottom', horizontalalignment='right',transform=ax.transAxes,color='green', fontsize=15)

            Efficacite = str(numpy.mean(bitrate_src))
            Efficacite = "Mean Bitrate: " + Efficacite[:7] + " (kbit/s)"
            ax2.text(0.95, 0.01, Efficacite,verticalalignment='bottom', horizontalalignment='right',transform=ax.transAxes,color='green', fontsize=15)



            fig.tight_layout()
            ax.grid()

            fig.savefig(srcname[:-3] + ".png")

            Score, frame, bitrate_src2 = Quality(pathoutref, index_ref2, pathoutsrc2, index_src2, length, methode[choose])

            with open(srcname2 +'.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Frame","Score", "Bitrate"])
                i = 0
                while (i < len(Score)):
                    writer.writerow([i,str(Score[i]).replace('.',','), str(bitrate_src2[i]).replace('.',',')])
                    i = i + 1
                if methode[choose] == "PSNR":
                    writer.writerow(["", "Mean PSNR (dB)", "Mean bitrate (Kb/s)"])
                if methode[choose] == "PY_PSNR":
                    writer.writerow(["", "Mean PSNR (dB)", "Mean bitrate (Kb/s)"])
                if methode[choose] == "SSIM":
                    writer.writerow(["", "Mean SSIM", "Mean bitrate (Kb/s)"])
                if methode[choose] == "VMAF":
                    writer.writerow(["", "Mean VMAF", "Mean bitrate (Kb/s)"])
                writer.writerow(["", "=MOYENNE(B2:B" + str(i + 1) + ")", "=MOYENNE(C2:C" + str(i + 1) + ")"])

            t = []
            for i in range(frame):
                t.append(i)
            print(len(t))
            fig, ax = plt.subplots()
            ax.set(title=srcname2)
            ax.set_xlabel("Frame")
            if methode[choose] == "PSNR" or methode[choose] == "PSNR":
                ax.set_ylabel('PSNR (dB)', color="tab:blue")
            if methode[choose] == "SSIM":
                ax.set_ylabel('SSIM', color="tab:blue")
            if methode[choose] == "VMAF":
                ax.set_ylabel('VMAF', color="tab:blue")
            ax.plot(t, Score, color="tab:blue")
            ax.tick_params(axis='y', color="tab:blue")

            ax2 = ax.twinx()
            ax2.set_ylabel('Bitrate (Kbit/s)', color="tab:red")
            ax2.plot(t, bitrate_src2, label='Bitrate', color="tab:red")
            ax2.tick_params(axis='y', color="tab:red")

            Efficacite = str(numpy.mean(Score))
            Efficacite = "Mean Score : " + Efficacite[:4] + " (dB)"
            ax2.text(0.95, 0.92, Efficacite, verticalalignment='bottom', horizontalalignment='right',
                     transform=ax.transAxes, color='green', fontsize=15)

            Efficacite = str(numpy.mean(bitrate_src2))
            Efficacite = "Mean Bitrate: " +Efficacite[:7] + " (kbit/s)"
            ax2.text(0.95, 0.01, Efficacite,verticalalignment='bottom', horizontalalignment='right',transform=ax.transAxes,color='green', fontsize=15)

            fig.tight_layout()
            ax.grid()

            fig.savefig(srcname2[:-3] + ".png")
            #plt.show()

            img1 = cv2.imread(srcname[:-3] + ".png")
            img2 = cv2.imread(srcname2[:-3] + ".png")
            side2side = numpy.hstack((img1, img2))
            cv2.imwrite(OUTPUTFILENAME + ".jpg", side2side)
            x=x+1

        done=time.time()-start
        print(done)


