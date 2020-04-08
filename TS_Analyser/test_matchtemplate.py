import cv2
import time
import numpy as np
import TS_Module as tools


template = cv2.imread('/home/moi/Images/vlcsnap-2020-03-05-15h03m19s964.png')#read ref frame
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) #convert frame in grayscale

matrix=[] #store SQDIFF scores

file='/home/moi/Documents/TIMOTHEE/jellyfish-15-mbps-hd-hevc.mkv'
cap = cv2.VideoCapture(file)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print('Number of frames: ' + str(length)  )

if (cap.isOpened()== False): 
  print("Error opening video stream or file")
start=time.time()

x=0
while(cap.isOpened()):
    ret, frame = cap.read()
    x=x+1
    if ret == True and x<=150: #limite search window to 150 frames
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        tmp = tools.match_template(frame,template)
        matrix.append(tmp)
    else:
        break

done=time.time()-start
cap.release()

print('The matching matrix: ')
#print(matrix)
print("Matrix's length: " + str(len(matrix)))
print('The best matching index is:')
print(matrix.index(min(matrix)))
print(done)

