
"""
# Ce code est plus efficace car ill utilise pas mediapipe mais bemol cest que on na pas la certitude de detecter une main, mais juste un truc de couleur la couleur dune main


import cv2
import numpy as np
from pynput.mouse import Controller as MouseController
from picamera2 import Picamera2
import time

width = 640 
height = 480

cam = Picamera2()
cam.start()

framerate = 30

# Créer une instance du contrôleur de souris
mouse = MouseController()

# Définir les limites pour la couleur de la peau dans l'espace de couleur HSV
lower_skin = np.array([0, 20, 70], dtype=np.uint8)
upper_skin = np.array([20, 255, 255], dtype=np.uint8)

# Fonction pour détecter et suivre la main
def detect_and_track_hand(frame):
    # Convertir l'image en espace de couleur HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Filtrer l'image pour ne garder que les pixels de couleur de peau
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Trouver les contours dans l'image filtrée
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Trouver le plus grand contour (assumant que c'est la main)
        max_contour = max(contours, key=cv2.contourArea)
        
        # Calculer le centre de la main
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Mettre à jour la position de la souris
            mouse.position = (cx, cy)
    
    # Afficher l'image avec le curseur
    cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Hand Tracking", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Hand Tracking", frame)

# Capture vidéo depuis la webcam
cap = cv2.VideoCapture(0)


while True :
    frame = cam.capture_array()
    frame = frame[ :, :, :3]
    blue, green, red = cv2.split(frame)
    frame = cv2.merge( [red, green, blue] )
    
    # Inverser l'image horizontalement pour que le mouvement de la main corresponde à celui de la souris
    frame = cv2.flip(frame, 1)
    
    x = (round(0.33*width) , round(0.33*height)) 
    y = (round(0.66*width) , round(0.66*height))
    c = (0 ,0 ,255 )
    
    cv2.line(frame, (x[0],0), (x[0],height), c, 1 )
    cv2.line(frame, (y[0],0), (y[0],height), c, 1 )
    cv2.line(frame, (0,x[1]), (width,x[1]), c, 1 )
    cv2.line(frame, (0,y[1]), (width,y[1]), c, 1 )
    
    # Appliquer la fonction de détection et de suivi de la main
    detect_and_track_hand(frame)
    
    # Quitter la boucle si la touche 'q' est enfoncée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cv2.imshow('Frame',frame)
    cv2.waitKey(1)
    time.sleep(1/framerate)
"""


# Alors que la jutilise mediapipe pour etre sur de tracker une main mais ca sera plus lent


import cv2
import numpy as np
from pynput.mouse import Controller as MouseController
from picamera2 import Picamera2
import mediapipe as mp
import time

width = 640 
height = 480

cam = Picamera2()
cam.start()

framerate = 30

# Créer une instance du contrôleur de souris
mouse = MouseController()



# Fonction pour détecter et suivre la main
def detect_and_track_hand(frame):
    
    lmList = []
    
    # Ensuite nous créons l’objet Hands
    mphands = mp.solutions.hands
    Hands = mphands.Hands()
    mp_Draw = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    results = Hands.process(frame) #Détecte la mains et récupère ses coordonnées
    
    # visualize
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Here is how we get the coordinates of the hand.
            for ids, landmark in enumerate(hand_landmarks.landmark):
                cx, cy = int(landmark.x*width), int(landmark.y*height)
                lmList.append([cx, cy])
            mp_Draw.draw_landmarks(frame, hand_landmarks, mphands.HAND_CONNECTIONS)
    
    
    # Calculer le centre de la main
    # on considere les points 2 et 17 de la main car leur milieu donne environ le centre de la main
    middle = [(lmList[2][0] + lmList[17][0])/2, (lmList[2][1] + lmList[17][1])/2] 

    # Mettre à jour la position de la souris
    mouse.position = (middle[0], middle[1])
    
    # Afficher l'image avec le curseur
    cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Hand Tracking", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Hand Tracking", frame)


while True :
    frame = cam.capture_array()
    frame = frame[ :, :, :3]
    blue, green, red = cv2.split(frame)
    frame = cv2.merge( [red, green, blue] )
    
    # Inverser l'image horizontalement pour que le mouvement de la main corresponde à celui de la souris
    frame = cv2.flip(frame, 1)
    
    x = (round(0.33*width) , round(0.33*height)) 
    y = (round(0.66*width) , round(0.66*height))
    c = (0 ,0 ,255 )
    
    cv2.line(frame, (x[0],0), (x[0],height), c, 1 )
    cv2.line(frame, (y[0],0), (y[0],height), c, 1 )
    cv2.line(frame, (0,x[1]), (width,x[1]), c, 1 )
    cv2.line(frame, (0,y[1]), (width,y[1]), c, 1 )
    
    # Appliquer la fonction de détection et de suivi de la main
    detect_and_track_hand(frame)
    
    # Quitter la boucle si la touche 'q' est enfoncée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cv2.imshow('Frame',frame)
    cv2.waitKey(1)
    time.sleep(1/framerate)





