#!/usr/bin/python

#----------------------------------------------------------------------------
# Face Detection Test (OpenCV)
#
# thanks to:
# http://japskua.wordpress.com/2010/08/04/detecting-eyes-with-python-opencv
#----------------------------------------------------------------------------

import cv2.cv as cv
import time
import Image

def DetectFace(image, faceCascade,min_size):

#    min_size = (20,20)
    image_scale = 2
    haar_scale = 1.2
    min_neighbors = 3
    haar_flags = 0

    
    # Allocate the temporary images
    grayscale = cv.CreateImage((image.width, image.height), 8, 1)
    smallImage = cv.CreateImage(
            (
                cv.Round(image.width / image_scale),
                cv.Round(image.height / image_scale)
            ), 8 ,1)

    # Convert color input image to grayscale
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)

    # Scale input image for faster processing
    cv.Resize(grayscale, smallImage, cv.CV_INTER_LINEAR)

    # Equalize the histogram
    cv.EqualizeHist(smallImage, smallImage)

    # Detect the faces
    faces = cv.HaarDetectObjects(
            smallImage, faceCascade, cv.CreateMemStorage(0),
            haar_scale, min_neighbors, haar_flags, min_size
        )

    # If faces are found
    if len(faces) > 1 or len(faces) == 0:
        return (None,None)
    
    if faces:
        for ((x, y, w, h), n) in faces:
            # the input to cv.HaarDetectObjects was resized, so scale the
            # bounding box of each face and convert it to two CvPoints
            x = int(x * image_scale)
            y = int(y * image_scale)
            w = int(w * image_scale)
            h = int(h * image_scale)
            cv.Rectangle(image, (x,y), (x+w,y+h), cv.RGB(255, 0, 0))
            
            copyImg = cv.CreateImage((w,h), 8, 1)
            src_region = cv.GetSubRect(grayscale, (x,y,w,h))
            cv.Copy(src_region, copyImg)
            cv.EqualizeHist(copyImg,copyImg)

            resized = cv.CreateImage((150,200),8,1)
            cv.Resize(copyImg, resized)
            
        return (image,min_size)

#----------
# M A I N
#----------


capture = cv.CaptureFromCAM(0)

#faceCascade = cv.Load("haarcascades/haarcascade_frontalface_default.xml")
faceCascade = cv.Load("haarcascades/haarcascade_frontalface_alt2.xml")
#faceCascade = cv.Load("haarcascades/haarcascade_frontalface_alt.xml")
#faceCascade = cv.Load("haarcascades/haarcascade_frontalface_alt_tree.xml")
#faceCascade = cv.Load("haarcascades/haarcascade_mcs_eyepair_big.xml")


#img = cv.LoadImage('me1.jpg')
#cv.ShowImage("Original",img)

#image = DetectFace(img, faceCascade)
i=0;
import sys
firstRun = True

while True:
    i+=1
#    if not i%50 == 0:
#        continue
    
    if not capture:
        print "Error opening capture device"
        sys.exit(1)
    image = cv.QueryFrame(capture)
    if image is None:
        break
    if firstRun:
        min_size = (20,20)
    (img,min_size) = DetectFace(image,faceCascade,min_size)
    if img is None:
        continue    
        
    cv.ShowImage("w1", img)
    i += 1
    k = cv.WaitKey(10)
 
    if k == 0x1b: # ESC
        print 'ESC pressed. Exiting ...'
        break