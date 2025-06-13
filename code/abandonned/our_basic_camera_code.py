

import cv2
from picamera2 import Picamera2
import time

width = 640 
height = 480

cam = Picamera2()
cam.start()

framerate = 30

while True :
    frame = cam.capture_array()
    frame = frame[ :, :, :3]
    blue, green, red = cv2.split(frame)
    frame = cv2.merge( [red, green, blue] )
    
    x = (round(0.1*width) , round(0.1*height)) 
    y = (round(0.9*width) , round(0.9*height))
    c = (0 ,0 ,255 )
    
    cv2.line(frame, (round(0.33*width),0), (round(0.33*width),height), (0,0,255), 1 )
    cv2.line(frame, (round(0.66*width),0), (round(0.66*width),height), (0,0,255), 1 )
    cv2.line(frame, (0,round(0.33*height)), (width,round(0.33*height)), (0,0,255), 1 )
    cv2.line(frame, (0,round(0.66*height)), (width,round(0.66*height)), (0,0,255), 1 )
    
    cv2.imshow('Frame',frame)
    cv2.waitKey(1)
    time.sleep(1/framerate)


