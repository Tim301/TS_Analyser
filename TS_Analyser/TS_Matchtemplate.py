import cv2
import time
import numpy as np
import TS_Module as tools

def gap_finder(ref, src, window):

    matrix=[] #store SQDIFF scores
    img_ref=None
    img_src=None

    cap = cv2.VideoCapture(ref)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('Number of frames: ' + str(length)  )
    
    if(cap.isOpened()):
        ret, template = cap.read() #Read first frame of Ref
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) #convert frame in grayscale
        img_ref=template
        font = cv2.FONT_HERSHEY_SIMPLEX
        txt = 'Image Reference index[0]'
        cv2.putText(img_ref,txt,(250,100), font, 2,(255,255,255),2)
    else:
        print("Error opening REF video stream or file")
        
    cap = cv2.VideoCapture(src)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('Number of frames: ' + str(length)  )

    if (cap.isOpened()== False): 
     print("Error opening video stream or file")
    start=time.time()

    x=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        x=x+1
        if ret == True and x<=window*25: #limite search window to 150 frames
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tmp = tools.match_template(frame,template)
            matrix.append(tmp)
            #cv2.imshow('Frame',frame)
            #print(matrix[len(matrix)-1])
            if matrix.index(min(matrix)) == (len(matrix)-1):
                img_src = frame
                font = cv2.FONT_HERSHEY_SIMPLEX
                txt = 'Image Source index['+ str(len(matrix)-1) + ']'
                cv2.putText(img_src,txt,(250,100), font, 2,(255,255,255),2)
                #print(matrix.index(min(matrix)))
            #cv2.waitKey(0)
        else:            
            break
            
    
    done=time.time()-start
    cap.release()
    
    img_ref = cv2.resize(img_ref, (0, 0), None, .5, .5)
    img_src = cv2.resize(img_src, (0, 0), None, .5, .5)
    
    side2side= np.hstack((img_ref, img_src))
    
    cv2.destroyAllWindows()
    print('The matching matrix: ')
    #print(matrix)
    print("Matrix's length: " + str(len(matrix)))
    print('The best matching index is:')
    print(matrix.index(min(matrix)))
    print(min(matrix))
    cv2.imshow('Resulatat',side2side)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return
