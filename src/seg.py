import cv2
import numpy as np
import os
import copy

def irisSegment(src):
    rows, cols, _ = src.shape
    cimg = copy.deepcopy(src)
    # Convert it to grayscale:
    srcGray = cv2.cvtColor( src,cv2.COLOR_BGR2GRAY)
    # Apply a Gaussian blur to reduce noise and avoid false circle detection:
    # srcBlur = cv2.GaussianBlur(srcGray,(5, 5),0)
    srcBlur = cv2.medianBlur(srcGray, 5)
    # Proceed to apply Hough Circle Transform:
    circles = cv2.HoughCircles(srcBlur, cv2.HOUGH_GRADIENT,1,20,param1=59,param2=63,minRadius=0,maxRadius=0)
    print(circles)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    # print(circles)
    # for circle in circles
    cv2.imshow('original', srcGray)
    cv2.imshow('blur', srcBlur)
    cv2.imshow('circles', cimg)
    cv2.waitKey(0)


if __name__ == "__main__":
    # generate paths
    myPath = os.path.abspath(os.path.dirname(__file__))
    imagePath = myPath + '\images'
    raw_images = os.listdir(imagePath)
    raw_images = list(map(lambda x:imagePath+'\\'+x, raw_images))
    image = cv2.imread(raw_images[0])

    # opencvPath = imagePath + '\opencv.png'
    # image = cv2.imread(opencvPath)

    irisSegment(image)

