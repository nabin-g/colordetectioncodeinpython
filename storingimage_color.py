print("START RUNNING PROGRAM")
import time
import serial
import cv2
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import requests
import base64

send = 0
time.sleep(10)

def beep(seconds,frame):
    ser=serial.Serial('/dev/serial0', 115200)
    send = 1
    cv2.imwrite('output.jpg',frame)
    with open ('output.jpg', 'rb') as imageFile:
        ans=base64 .b64encode(imageFile.read())
    ser.write(ans)
    #print (ans)
    time.sleep(0.5)
    print("Sending photo...")
#default range
a = 300
b = 480
c = 180
d = 470

xxx = 0
yyy = 0
rrr = 0
cali = 0


k = 0

while True:
    for i in range(10):
        boardname = '/dev/ttyACM'+str(i)
        #print(boardname)
        try:
            ser=serial.Serial(boardname, 115200)
            importdata=ser.readline()
            importdata=importdata.decode('utf-8')
            break
        except:
            continue
    try:
        if importdata:
            pass
    except:
        continue
        
    #ser=serial.Serial('/dev/ttyACM1', 115200)
    # ser=serial.Serial('/dev/ttyACM2', 115200)
    #print(importdata)
    length=len(importdata)
    #print(length)
    if(length==18):
        outcome=importdata.split(":")
        #print(outcome[0])
        #if(str(outcome[0])=="Vibration 1"):
            #print (float(outcome[1]))
        try:
            if(float(outcome[1]) > float(0.2)):
                pass
        except:
            continue
        if(float(outcome[1]) > float(0.2)):
            for i in range(10):
                image = cv2.VideoCapture(i)
                if image.isOpened():
                    break
            keynum = 0
            sumofva = 0.00
            while (image.isOpened()):
                #print("321")
                if (keynum<10):
                    try:
                        importdata=ser.readline()
                        importdata=importdata.decode('utf-8')
                        outcome=importdata.split(":")
                        sumofva += float(outcome[1])
                        keynum += 1
                    except:
                        pass
                else:
                    print(sumofva)
                    keynum = 0
                    if float(sumofva/10)>2:
                        sumofva = 0
                        continue
                    else:
                        sumofva = 0
                        break   
                
                
                for i in range(6):
                    ret, frame2 = image.read()
                frame = cv2.resize(frame2,(100,80))
                flag = 0
                #frame2 = frame2[c:d,a:b]
                #frame2 = cv2.resize(frame,(50,25))
                for i in range(79):
                    for j in range(100):
                        if flag>=200:
                            continue
                        #150 40 40 do not delete this line!
                        try:
                            if int(frame[i,j][2])/(int(frame[i,j][0])+int(frame[i,j][1]))>0.7 and int(frame[i,j][2])>130:
                        #if frame2[i,j][2]>130 and frame2[i,j][0]<100 and frame2[i,j][1]<100:
                            #print(frame[i,j])
                                flag += 1
                            else:
                                pass
                        except:
                            pass
                            #frame[i,j][0] = 255
                            #frame[i,j][1] = 255
                            #frame[i,j][2] = 255
                #print("flag")
                #cv2.imshow("Output", frame)
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #    break
                print(flag)
                if (flag>=200): 
                    beep(0.05,frame)
                    time.sleep(2)     
            

