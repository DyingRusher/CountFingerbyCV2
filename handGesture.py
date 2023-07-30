import cv2
import time
import os
import handTrackingModule as htm

cap = cv2.VideoCapture(0)
cap.set(3,1000)
cap.set(4,800)

dectector = htm.handTracker()


##getting imgs 
folderPath = "countFingureImg"
imgs = os.listdir(folderPath)
savImg = []
# print(imgs)
for im in imgs:
    image = cv2.imread(f'{folderPath}/{im}')
    print(im)
    savImg.append(image)

# print(savImg)
pTime = 0

tipIds = [8,12,16,20]
while True:

    success , img = cap.read()

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    img = dectector.findHands(img)

    lmList = dectector.findPosition(img,True,[8,6,12,10,16,14,20,18])
    # print(lmList)


    ##counting figures
    if len(lmList)!=0:
        fingers = []

        if lmList[4][1] > lmList[2][1]:
            fingers.append(0)
        else:
            fingers.append(1)

        for id in range(0,4):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
            
        totalFig = fingers.count(1)
        img[0:400,0:300] = savImg[totalFig]
        print(totalFig)

    cv2.putText(img,f'fps{str(int(fps))}',(400,100),cv2.FONT_ITALIC,2,(32,243,0),3)

    interrupt = cv2.waitKey(1)
    if interrupt & 0xFF == 27:
        break 
    cv2.imshow("sd",img)