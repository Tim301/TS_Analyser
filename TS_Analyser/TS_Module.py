import os, json
import subprocess
import csv
import cv2


def getInfo(filepath):
    result = subprocess.run(['ffprobe', '-show_programs', '-of', 'json', '-v', 'quiet', '-i', filepath], stdout=subprocess.PIPE)
    result=result.stdout.decode('utf-8')
    ts_info=json.loads(result)
    return ts_info

def exportInfo(filename,ts_info):
    filename=filename+'.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["CHANNEL:", "PROGRAM ID:", "VIDEO FORMAT:"])
        j = len(ts_info['programs'])
        for i in range(j):
        #print(ts_info['programs'][i]['tags']['service_name'])
            try:
                name=ts_info['programs'][i]['tags']['service_name']
            except:
                name='NC'
            try:
                tsid = ts_info['programs'][i]['program_id']
            except:
                tsid='NC'
            try:
                k=0
                while (ts_info['programs'][i]['streams'][k]['codec_type']=='Video') and (k<=len(ts_info['programs'][i]['streams'])):
                    print(len(ts_info['programs'][i]['streams']))
                    k=k+1
                vformat =str(ts_info['programs'][i]['streams'][k]['width'])+'x'+ str(ts_info['programs'][i]['streams'][k]['height'])
            except:
                vformat = 'NC'
            writer.writerow([name,tsid,vformat])
    print('Done')
    
def PSNR(filepath,vref,vdeg):
    filename = getFilename(filepath)
    output= 'psnr='+filename
    print(output)
    print('Work in progress')
    result = subprocess.run(['ffmpeg', '-i', vref, '-i', vdeg, '-lavfi', output, '-f', 'null', '-'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    #result=result.split('\r\n')
    print('PSNR done')
    print(result)

def to_raw(filepath):
    filename = '%06d.tif'
    print(filename)
#    k=0
#    while (video['programs'][i]['streams'][k]['codec_type']=='Video'):
#        k=k+1
#    ips=video['programs'][i]['streams'][k]['r_frame_rate']
#    print(ips)
    output = '/tmp/testvideo/'+filename
    subprocess.run(['ffmpeg', '-t', '10', '-i',filepath,'-start_number', '30', output])
    
def getFilename(filepath):
    filename=os.path.basename(os.path.normpath(filepath))
    return(filename)

def get_length(filepath):
    cap = cv2.VideoCapture(filepath)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return length # in frames

#get similarity of a frame
def match_template(img,template):
    res = cv2.matchTemplate(img,template,0)
    return(res[0][0]) #return SQDIFF score

def ts_id(json,nb):
    tsid=[]
    try:
        for i in range(nb):
            tsid.append(json['programs'][i]['program_id'])
        return tsid
    except:
        return tsid

def tsExtract(pathin, pathout, mapindex):
    index= "0:" + str(mapindex)
    subprocess.run(['ffmpeg', '-y', '-nostats', '-loglevel', '0','-i', pathin, '-c:v', 'copy', '-map', index, pathout])
    
def mapinfo(ts_info):
    mapIndex=[]
    try:
        j = len(ts_info['programs'])
        for i in range(j):        
            k=0
            while (ts_info['programs'][i]['streams'][k]['codec_type']!='video') and (k<=len(ts_info['programs'][i]['streams'])):
                k=k+1
            if (ts_info['programs'][i]['streams'][k]['codec_type']=='video') and (k<=len(ts_info['programs'][i]['streams'])):
                mapIndex.append(ts_info['programs'][i]['streams'][k]['index'])
            elif (k==len(ts_info['programs'][i]['streams'])):
                mapIndex.append('NoVideo')
        return mapIndex
    except:
        mapIndex = 'Error'
        return mapIndex
