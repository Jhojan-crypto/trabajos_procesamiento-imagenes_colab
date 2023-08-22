import sys
import cv2
import numpy as np

rsegmentacion = 'input75.jpg'

# Dibujar un rectángulo basado en la selección de entrada
def draw_rectangle(event, x, y, flags, params):
    global x_init, y_init, drawing, top_left_pt, bottom_right_pt, img_orig
    # Detectar un evento de botón del mouse presionado
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_init, y_init = x, y
    # Detectando el movimiento del mouse
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            top_left_pt, bottom_right_pt = (x_init, y_init), (x,y)
            img[y_init:y, x_init:x] = 255 - img_orig[y_init:y, x_init:x]
            cv2.rectangle(img, top_left_pt, bottom_right_pt, (0,255,0), 2)
    # Detectar evento de botón del mouse hacia arriba
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        top_left_pt, bottom_right_pt = (x_init,y_init), (x,y)
        img[y_init:y, x_init:x] = 255 - img[y_init:y, x_init:x]
        cv2.rectangle(img, top_left_pt, bottom_right_pt, (0,255,0), 2)
        rect_final = (x_init, y_init, x-x_init, y-y_init)
        # Ejecute Grabcut en la región de interés
        run_grabcut(img_orig, rect_final)

# Algoritmo Grabcut
def run_grabcut(img_orig, rect_final):
    # Initialize the mask
    mask = np.zeros(img_orig.shape[:2],np.uint8)
    # Extract the rectangle and set the region of
    # interest in the above mask
    x,y,w,h = rect_final
    mask[y:y+h, x:x+w] = 1
    # Initialize background and foreground models
    bgdModel = np.zeros((1,65), np.float64)
    fgdModel = np.zeros((1,65), np.float64)
    # Run Grabcut algorithm
    cv2.grabCut (img_orig, mask, rect_final, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    # Extract new mask
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    # Apply the above mask to the image
    img_orig = img_orig*mask2[:,:,np.newaxis]
    # Display the image
    cv2.imshow('Output', img_orig)

if __name__ == '__main__':
    drawing = False
    top_left_pt, bottom_right_pt = (-1,-1), (-1,-1)
    # Read the input image
    img_orig = cv2.imread(rsegmentacion)
    img = img_orig.copy()
    cv2.namedWindow('Input')
    cv2.setMouseCallback('Input', draw_rectangle) 
    while True:
        cv2.imshow('Input', img)
        c = cv2.waitKey(1)
        if c == 27:
            break
    cv2.destroyAllWindows()