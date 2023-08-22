import sys
import cv2
import numpy as np
refpt = []

cropping = False

def cortar (event, x, y, flags, params):
    global refpt, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x,y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x,y))
        cropping = False
        cv2.rectangle(clonel, refPt[0], refPt[1], (0,255,0), 2)
        cv2.imshow('image', clonel)

#image =cv2.imread('./images/input.jpg')
n = '75'
image = cv2.imread('input'+str(n)+'.jpg')

#for i in range(25):
for i in range(10):

    x,y,z = np.shape(image)

    clonel = cv2.resize(image,(1033,240), interpolation=cv2.INTER_AREA)
    #clonel = cv2.resize(image,(160,400), interpolation=cv2.INTER_AREA)

    clone = clonel.copy()
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', cortar)

    while True:
        cv2.imshow('image', clonel)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("r"):
            clonel = clone.copy()
            print("recorte nuevamente la imagen")
        if key == ord("c"):
            print("imagen cortada presione tecla para continuar")
            break
    
    if len(refPt) == 2:
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        roil = cv2.resize(roi,(150,385), interpolation = cv2.INTER_AREA)

        #cv2.imwrite('marcador'+str(i)+'.jpg',roil)
        #i = i + 79
        cv2.imwrite('marcador'+str(n)+str(i)+'.jpg',roil)

        cv2.waitKey(0)
        print('Completado...')
        cv2.destroyAllWindows()