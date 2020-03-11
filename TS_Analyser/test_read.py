import numpy as np
import cv2
import argparse

file='/home/moi/go/VLC/fff.mp4'
cap = cv2.VideoCapture(file)
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

while(cap.isOpened()):
    ret, frame = cap.read() 
    if ret == True:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Frame',frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else: 
        break
cap.release()
cv2.destroyAllWindows()