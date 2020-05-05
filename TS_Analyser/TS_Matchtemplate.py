import cv2
import time
import numpy as np
import TS_Module as tools

def gap_finder(ref,ref_name, src, src_name,window, debug):

    matrix=[] #store PSNR scores
    matrix2=[] #store PSNR scores
    img_ref=None
    img_src=None
    img_ref2=None
    img_src2=None

    height = None
    width = None
    depth = None


    cap = cv2.VideoCapture(ref)
    
    if(cap.isOpened()):
        ret, template = cap.read() #Read first frame of Ref
        height, width, depth = template.shape
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) #convert frame in grayscale
        img_ref=template
        if debug:
            font = cv2.FONT_HERSHEY_SIMPLEX
            txt1 = ref_name  + 'index[0] '+ '\n'
            cv2.putText(img_ref,txt1,(250,100), font, 2,(0,0,255),2)
    else:
        print("Error opening REF video stream or file")

    cap = cv2.VideoCapture(src)

    if (cap.isOpened()== False): 
     print("Error opening video stream or file")
    start=time.time()

    x=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        x=x+1
        if ret == True and x<=window*25: #limite search window to 150 frames
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame,(width,height))
            tmp = tools.match_template(frame,template)
            matrix.append(tmp)
            if matrix.index(min(matrix)) == (len(matrix)-1) and debug:
                img_src = frame
                if debug:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    txt1 = src_name + 'index['+ str(len(matrix)-1)  + '] '+ '\n'
                    cv2.putText(img_src,txt1,(250,100), font, 2,(0,0,255),2)

        else:            
            break
    min1 = min(matrix)

    cap2 = cv2.VideoCapture(src)
    if (cap.isOpened()):
        ret, template = cap2.read()  # Read first frame of Src
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)  # convert frame in grayscale
        template = cv2.resize(template, (width, height))
        img_src2 = template
        if debug:
            font = cv2.FONT_HERSHEY_SIMPLEX
            txt1 = src_name + ' index[0] ' + '\n'
            cv2.putText(img_src2, txt1, (250, 100), font, 2, (0, 0, 255), 2)
    else:
        print("Error opening REF video stream or file")

    cap2 = cv2.VideoCapture(ref)

    if (cap2.isOpened() == False):
        print("Error opening video stream or file")
    start = time.time()

    x = 0
    while (cap2.isOpened()):
        ret, frame = cap2.read()
        x = x + 1
        if ret == True and x <= window * 25:  # limite search window to 150 frames
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame, (width, height))
            tmp = tools.match_template(frame, template)
            matrix2.append(tmp)
            if matrix2.index(min(matrix2)) == (len(matrix2) - 1) and debug:
                img_ref2 = frame
                if debug:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    txt1 = ref_name + ' index[' + str(len(matrix2) - 1) + '] ' + '\n'
                    cv2.putText(img_ref2, txt1, (250, 100), font, 2, (0, 0, 255), 2)

        else:
            break
    min2 = min(matrix2)

    if min2 < min1 :
        inversed = True
    else:
        inversed = False
    print(inversed)

    if debug:
        done=time.time()-start
        cap.release()
        cap2.release()

        if inversed:
            print(img_ref2.shape)
            print(img_src2.shape)
            img_ref2 = cv2.resize(img_ref2, (0, 0), None, .5, .5)
            img_src2 = cv2.resize(img_src2, (0, 0), None, .5, .5)
            side2side = np.hstack((img_ref2, img_src2))
        else:
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
        cv2.imwrite(src_name + ".jpg", side2side)
        cv2.imshow('Resultat: ',side2side)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if inversed:
        return matrix2.index(min(matrix2)),0
    else:
        return 0,matrix.index(min(matrix))
