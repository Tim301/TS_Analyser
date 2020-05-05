import cv2
import time
import numpy as np
import TS_Module as tools
from bitrate import getBitrate

from skimage.measure import compare_ssim as ssim

def Quality(ref, index_ref, src, index_src, window, choosen):
    Score = []  # store Score scores
    Quality = [] # store Score/bitrate
    Bitrate = []
    img_ref = None
    img_src = None

    height = None
    width = None
    depth = None

    if index_ref > index_src:
        index= index_ref
    else:
        index= index_src

    cap_ref = cv2.VideoCapture(ref)
    ref_depth = 8
    cap_src = cv2.VideoCapture(src)
    bitrate_src = getBitrate(src, window)
    src_depth = 8

    if (ref_depth != src_depth):
        print("Error Ref and Scr doesn't have the same bit depth")
    else:
        if (cap_ref.isOpened() and cap_src.isOpened()):
            x = 0
            x_ref=0 # Read first frame of Ref
            ret_ref, template_ref = cap_ref.read()
            height, width, depth = template_ref.shape

            while(x_ref != index_ref ):
                ret_ref, template_ref = cap_ref.read()
                x_ref = x_ref + 1
            x_src = 0  # Read first frame of Ref
            ret_src, template_src = cap_src.read()

            while (x_src != index_src):
                ret_src, template_src = cap_src.read()
                template_src = cv2.resize(template_src,(width,height))
                x_src = x_src + 1

            while(ret_ref == True and ret_src == True and x<=window-index-1):
                ret_ref, template_ref = cap_ref.read()
                ret_src, template_src = cap_src.read()
                template_src = cv2.resize(template_src, (width, height))
                img_ref = cv2.cvtColor(template_ref, cv2.COLOR_BGR2YUV)
                img_ref = img_ref[:,:,0]
                img_src = cv2.cvtColor(template_src, cv2.COLOR_BGR2YUV)
                img_src = img_src[:,:,0]
                if choosen == "PSNR":
                    result_static = cv2.PSNR(img_ref, img_src)
                    Score.append(result_static)
                    Bitrate.append(bitrate_src[x_src])
                if choosen == "SSIM":
                    result_static = ssim(img_ref, img_src)
                    Score.append(result_static)
                    Bitrate.append(bitrate_src[x_src])
                if choosen == "Py_PSNR":
                    Score.append(tools.calculate_psnr(img_ref,img_src, ref_depth))
                    Bitrate.append(bitrate_src[x_src])

                x= x+ 1
                x_ref = x_ref + 1
                x_src = x_src + 1

    print("Score")
    print(Score)
    print("Bitrate")
    print("Results")
    print(Quality)

    return Score, x, Bitrate
