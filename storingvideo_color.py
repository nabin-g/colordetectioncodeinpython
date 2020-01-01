# importing the necessary packages
from collections import deque
import numpy as np
import imutils
import os
import sys 
import cv2
import urllib #for reading image from URL

import time
# duration in seconds of the video capture

capture_duration = 30


# to the webcam
camera = cv2.VideoCapture(0)
 
# define the lower and upper boundaries of the colors in the HSV color space
lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)} #assign new item lower['blue'] = (93, 10, 0)
upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}
 
# define standard colors for circle around the object
colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255)}

#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
fourcc = cv2.cv.CV_FOURCC(*'MJPG')
#x=str(time.time())+'video.avi'
#rec = cv2.VideoWriter(x, fourcc, 5, (640, 480))
name = os.path.join(os.getcwd(), "VIDEOS")
#print (name)
start_time=time.time()
x=os.path.join(name ,str(int (time.time()))+'video.avi')
rec = cv2.VideoWriter(str(x), fourcc, 5, (640, 480))
# keep looping
while camera.isOpened():
    
    
    
    # grab the current frame
    #while( int(time.time() - start_time) < capture_duration ):
        
    
    grabbed, frame1 = camera.read()
    
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame1, width=600)
    
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary`1, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
               
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
            # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 0.5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                #cv2.imwrite("output.jpg", frame)
                
                cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                cv2.putText(frame,key , (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
                #repeating interval of video recorded
                if(int(time.time() - start_time) >= capture_duration):
                    start_time=time.time()
                    x=os.path.join(name ,str(int (time.time()))+'video.avi')
                    rec = cv2.VideoWriter(str(x), fourcc, 5, (640, 480))
                
                rec.write(frame1)       
     
        # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        rec.release()
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
