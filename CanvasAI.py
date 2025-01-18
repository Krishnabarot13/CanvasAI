import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

import HandTrackingModule as htm
brushThickness=15
eraserThickness=200

folderpath="Header"
mylist=os.listdir(folderpath)
print(mylist)
overlaylist=[]

for imgPath in mylist:
    image=cv2.imread(f'{folderpath}/{imgPath}')
    overlaylist.append(image)
print(len(overlaylist))

header=overlaylist[0]
drawColor=(0,128,255)

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=htm.handDetector(detectionCon=0.85)
xp,yp=0,0
imgCanvas=np.zeros((720,1280,3),np.uint8)

while True:
    #import the image
    success,img=cap.read()
    img=cv2.flip(img,1)

    #2.find hand land marks
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        # print(lmList)
        #tip of index and middle finger
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        #3.checking which fingures are up.
        fingures=detector.fingersUp()
        print("fingures: ",fingures)
        #4.if selection mode-2 fingures are up-then we have to select not draw.
        if fingures[1] and fingures[2]:
            xp,yp=0,0
            
            print("Selection mode")
            if y1<125:
                if 207<=x1<=418:
                    header=overlaylist[0]
                    drawColor=(0,128,255)
                #550 750
                elif 440<=x1<=638:
                    header=overlaylist[1]
                    drawColor=(0,204,0)
                elif 640<=x1<=856:
                    header=overlaylist[2]
                    drawColor=(148,0,211)
                elif 860<=x1<=1060:
                    header=overlaylist[3]
                    drawColor=(255,165,0)
                elif 1060<=x1<=1260:
                    header=overlaylist[4]
                    drawColor=(0,0,0)
                cv2.rectangle(img,(x1,y1-25),(x2,y2+25),(255,0,255),cv2.FILLED)
        
        #5.if drawing mode when index finger is up.
        if fingures[1] and fingures[2]==False:

            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
            xp,yp=x1,y1
    
            print("Drawing mode")
    grayImage=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv=cv2.threshold(grayImage,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)

    




    #setting the header image
    header_resized = cv2.resize(header, (1280, 125))  # Resize to (125, 1280, 3)
    img[0:125, 0:1280] = header_resized
    # img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    # img[0:125,0:1280]=header
    cv2.imshow("image: ",img)
    cv2.imshow("Canvas: ",imgCanvas)
    cv2.waitKey(1)

# pTime=0
# cTime=0
# cap=cv2.VideoCapture(0)
# detector=htm.handDetector()

# while True:
#     success,img=cap.read()
#     img=detector.findHands(img)
#     lmList=detector.findPosition(img)
#     if len(lmList)!=0:
#         print(lmList[4])
                        
#     cTime=time.time()
#     fps=1/(cTime-pTime)
#     pTime=cTime
#     cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)

#     cv2.imshow("Image ",img)
#     cv2.waitKey(1)