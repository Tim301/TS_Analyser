import numpy as np
import cv2
import argparse

window = 5

global img

template = cv2.imread('/home/moi/Images/vlcsnap-2020-03-05-15h03m19s964.png')

file='/tmp/ts/01c-ATEME-16s-h264mixte.ts'
cap = cv2.VideoCapture(file)
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

log_error=[]

x=0
while(cap.isOpened()):
    ret, frame = cap.read()
    x=x+1
    if ret == True and x<=window*25:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        log_error.append(x)
        if x==10:
            img = frame
            #cv2.imshow('IMG',img)
        #cv2.imshow('Frame',frame)        
        while cv2.getWindowProperty('just_a_window', cv2.WND_PROP_VISIBLE) >= 1:
        keyCode = cv2.waitKey(wait_time)
        if (keyCode & 0xFF) == ord("q"):
            cv2.destroyAllWindows()
            break
    else: 
        break
cap.release()

print(log_error)
print(cap.isOpened())
#print(img.shape)
cv2.imshow('IMG 2',img)



#cv2.destroyAllWindows()