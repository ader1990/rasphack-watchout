#!/usr/bin/python
"""
This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
"""
import sys
import cv2.cv as cv
from optparse import OptionParser
import pyfirmata #pt legatura cu Arduino # Creeaza un obiect Arduino pe portul specificat
import random
import time
board = pyfirmata.Arduino('/dev/ttyACM0') #Pinii Arduino pt motoare (ca variabile)
PIN_stanga_inainte = board.get_pin('d:5:p') #pinul digital 5 = pwm
PIN_stanga_inapoi = board.get_pin('d:3:p')
PIN_dreapta_inainte = board.get_pin('d:6:p')
PIN_dreapta_inapoi = board.get_pin('d:9:p') # Pornim un thread Iterator care sa se ocupe de datele pe serial (pt analog)
left=0;
right=0;
max_speed=900.0;

def mergi(stanga, dreapta):
    if(stanga > 0):
            PIN_stanga_inapoi.write(0)
            PIN_stanga_inainte.write(stanga/max_speed)
    else:
            PIN_stanga_inapoi.write(-stanga/max_speed)
            PIN_stanga_inainte.write(0)
            if(dreapta > 0):
                PIN_dreapta_inapoi.write(0)
                PIN_dreapta_inainte.write(dreapta/max_speed)
            else:
                PIN_dreapta_inapoi.write(-dreapta/max_speed)
                PIN_dreapta_inainte.write(0)
#while (1):
#    if(random.random()  < 0.5):
#        left+=random.random()*150/10;
#        mergi(-left,-left) #inainte
#        time.sleep(0.001)
#    else:
#        right+=random.random()*150/10;
#        mergi(-right, right) #inainte
#        time.sleep(0.001)



# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned 
# for accurate yet slow object detection. For a faster operation on real video 
# images the settings are: 
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
# min_size=<minimum possible face size

min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = cv.CV_HAAR_DO_CANNY_PRUNING

def detect_and_draw(img, cascade):
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
			       cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    #cv.EqualizeHist(small_img, small_img)
    image=img
    cv.SetImageCOI(image,1)
    cv.SetImageCOI(image,0)

    hsv=cv.CreateImage(cv.GetSize(image), 8, 3)
    h_plane=cv.CreateImage(cv.GetSize(image), 8, 1)
    s_plane=cv.CreateImage(cv.GetSize(image), 8, 1)
    cv.CvtColor(image, hsv, cv.CV_RGB2HSV)
    cv.Split(hsv, h_plane, s_plane, None, None)
    #img=s_plane;
	
    mergi(0,0)
    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
            mergi(-100,-100)
            mergi(-100,100)
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the 
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
#        else
#            mergi(0,0)
       
    cv.ShowImage("result", img)

if __name__ == '__main__':

    parser = OptionParser(usage = "usage: %prog [options] [filename|camera_index]")
    parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default = "../data/haarcascades/haarcascade_frontalface_alt.xml")
    (options, args) = parser.parse_args()

    cascade = cv.Load(options.cascade)
    
    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    input_name = args[0]
    if input_name.isdigit():
        capture = cv.CreateCameraCapture(int(input_name))
    else:
        capture = None

    cv.NamedWindow("result", 1)

    width = 320 #leave None for auto-detection
    height = 240 #leave None for auto-detection

    if width is None:
    	width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
    else:
    	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    

    if height is None:
	height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
    else:
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 

    if capture:
        frame_copy = None
        while True:

            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(0)
                break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)

#                frame_copy = cv.CreateImage((frame.width,frame.height),
#                                            cv.IPL_DEPTH_8U, frame.nChannels)

            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)
            
            detect_and_draw(frame_copy, cascade)

            if cv.WaitKey(10) >= 0:
                break
    else:
        image = cv.LoadImage(input_name, 1)
        detect_and_draw(image, cascade)
        cv.WaitKey(0)

    cv.DestroyWindow("result")
