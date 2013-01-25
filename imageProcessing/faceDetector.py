#!/usr/bin/env python

#----------------------------------------------------------------------------
# Face Detection Test (OpenCV)
#
# thanks to:
# http://japskua.wordpress.com/2010/08/04/detecting-eyes-with-python-opencv
#----------------------------------------------------------------------------

import cv2.cv as cv
import time
import Image
import sys,os,traceback


class faceDetector(object):
    def __init__(self,inputDir,outputDir):
        haarFolder = 'imageProcessing/'
        self.faceCascade = cv.Load(haarFolder+'haarcascades/haarcascade_frontalface_default.xml')
#        self.faceCascade = cv.Load(haarFolder+'haarcascades/haarcascade_frontalface_alt2.xml')

        self.inputDir = inputDir 
        self.outputDir = outputDir
        
    
    def run(self):    
        files=[]
        for afile in os.listdir(self.inputDir):
            if afile[-3:] != 'jpg':
                continue
            print afile
            files.append(afile)
        files.sort()
        for afile in files:
            print (afile)
            img = None
            image = cv.LoadImage(self.inputDir + afile)
            if image is None:
                raise ValueError,'Image not loaded?!?'
            try:            
                (img,min_size) = self.DetectFace(image,self.faceCascade)
            except:
                print img
                traceback.print_exc(file=sys.stdout)
            if img is None:
                continue    
            cv.SaveImage(self.outputDir + afile[0:-4]+'_procced.jpg', img)    
            
    def DetectFace(self,image, faceCascade):
    
        min_size = (10,10)
        image_scale = 1
        haar_scale = 1.1
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
#        if len(faces) > 1 or len(faces) == 0:
#            return (None,None)
        
        if faces:
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                x = int(x * image_scale)
                y = int(y * image_scale)
                w = int(w * image_scale)
                h = int(h * image_scale)
                
                copyImg = cv.CreateImage((w,h), 8, 1)
                src_region = cv.GetSubRect(grayscale, (x,y,w,h))
                cv.Copy(src_region, copyImg)
#                cv.EqualizeHist(copyImg,copyImg)
    
                resized = cv.CreateImage((150,200),8,1)
                cv.Resize(copyImg, resized)
            return (resized,min_size)

#----------
# M A I N
#----------
if __name__ == '__main__':
    import sys
    inputDir = outputDir = sys.argv[1]
    fd = faceDetector(inputDir,outputDir)
    fd.run()
