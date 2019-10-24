import cv2
import numpy as np
import os
import copy

def irisSegment(src):
    rows, cols, _ = src.shape
    # Convert it to grayscale:
    srcGray = cv2.cvtColor( src,cv2.COLOR_BGR2GRAY)
    # Apply a Gaussian blur to reduce noise and avoid false circle detection:
    # srcBlur = cv2.GaussianBlur(srcGray,(5, 5),0)
    srcBlur = cv2.medianBlur(srcGray, 5)
    # detect edges
    srcEdge = cv2.Canny(srcBlur, 40, 40)
    # do dilation
    kernel = np.ones((30,30),np.uint8)
    srcDia = cv2.dilate(srcEdge,(3,3),iterations = 1)

    # First binarize the image so that findContours can work correctly.
    _, thresh = cv2.threshold(srcBlur, 127, 255, cv2.THRESH_BINARY)
    # Now find the contours and then find the pupil in the contours.
    contours, _, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Proceed to apply Hough Circle Transform:
    circles = cv2.HoughCircles(srcBlur, cv2.HOUGH_GRADIENT,1,20,param1=59,param2=63,minRadius=0,maxRadius=0)
    # circles = cv2.HoughCircles(contours, cv2.HOUGH_GRADIENT,1,20)
    print(circles)

    # draw the circles
    circles = np.uint16(np.around(circles))
    cimg = copy.deepcopy(src)
    for i in circles[0,:]:
        # print()
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    # print(circles)
    # for circle in circles
    # cv2.imshow('original', srcGray)
    cv2.imshow('blur', srcBlur)
    # cv2.imshow('contours', contours)
    cv2.imshow('circles', cimg)
    cv2.waitKey(0)


if __name__ == "__main__":
    # generate paths
    myPath = os.path.abspath(os.path.dirname(__file__))
    imagePath = myPath + '\images'
    raw_images = os.listdir(imagePath)
    raw_images = list(map(lambda x:imagePath+'\\'+x, raw_images))
    image = cv2.imread(raw_images[0])

    # for image in raw_images:
    #     image = cv2.imread(image)

    # opencvPath = imagePath + '\opencv.png'
    # image = cv2.imread(opencvPath)

    irisSegment(image)

