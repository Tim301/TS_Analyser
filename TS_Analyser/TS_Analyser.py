import os
import TS_Module as tools

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

file='01c-ATEME-16s-h264mixte.trp'
filepath = os.path.join(BASE_DIR,file)
#print(tools.getFilename(filepath))

#Get ts info from filepath
if os.path.isfile(filepath):
    ts_info=tools.getInfo(filepath)
    tools.exportInfo("ts_info",ts_info)
    #print channels available
    
else:
    print('Error getting file info')

vref=os.path.join(BASE_DIR,'jellyfish-15-mbps-hd-hevc.mkv')
vdeg=os.path.join(BASE_DIR,'jellyfish-3-mbps-hd-hevc.mkv')


#tools.PSNR('psnrtext.txt',vref,vdeg)
#tools.toRaw(vref)