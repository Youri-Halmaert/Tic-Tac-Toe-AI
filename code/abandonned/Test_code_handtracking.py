

# Specification for the user : the palm of your hand must ALWAYS be the side facing the camera, otherwise the camera wont be able to tell if its your left or right hand youre using.
# Advantage : this way, the player can use both his hands, this is a very inclusive thing to do because this enables people with one hand mising to still be able to play 


from picamera2 import Picamera2
import cv2 as cv
import mediapipe as mp
import numpy as np
import time

# On crée aussi l’objet drawing_utils que nous utiliserons pour pouvoir tracer des lignes représentant la forme de la main sur celles détectés sur chaque frame de la vidéo
mp_Draw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Maintenant qu’on a la vidéo, on va créer l’objet hands qui nous permettra de détecter la main droite et gauche sur la vidéo ainsi que de récupérer les différents coordonnées de ces derniers.
mphands = mp.solutions.hands

width = 900 
height = 900

# get video frames
cam = Picamera2()
config = cam.create_preview_configuration({"size":(width,height)})
cam.configure(config)
cam.start()

framerate = 30


# Ensuite nous créons l’objet Hands
Hands = mphands.Hands()

# a bunch of useful lists
lmList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
tipIds = [4, 8, 12, 16, 20]
side_of_hand = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
middle = [0,0]

totalFingers = 0

# the function that enables to highlight the chosen cell
def highlight_cell(frame, x, y, w, h):
    
    overlay = frame.copy()
    cv.rectangle(overlay, (x,y), (x+w, y+h), (0, 200, 0), -1)
    alpha = 0.4
    return cv.addWeighted(overlay, alpha, frame,1-alpha,0)



while True :
    frame = cam.capture_array()
    frame = frame[ :, :, :3]
    blue, green, red = cv.split(frame)
    frame = cv.merge( [red, green, blue] )
    
    # Flips the image the camera returns for a more intuitive experience for the user.
    frame = cv.flip(frame,1)
    
    x = (round(0.33*width) , round(0.33*height)) 
    y = (round(0.66*width) , round(0.66*height))
    c = (0 ,0 ,255 )
    
    cv.line(frame, (x[0],0), (x[0],height), c, 1 )
    cv.line(frame, (y[0],0), (y[0],height), c, 1 )
    cv.line(frame, (0,x[1]), (width,x[1]), c, 1 )
    cv.line(frame, (0,y[1]), (width,y[1]), c, 1 )
    
    # detect objects and track objects
    #Traçage des lignes (Ca va dans la boucle true)
    results = Hands.process(frame) # Détecte la mains et récupère ses coordonnées
    
    # visualize
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Here is how we get the coordinates of the hand.
            for ids, landmark in enumerate(hand_landmarks.landmark):
                cx, cy = int(landmark.x*width), int(landmark.y*height)
                lmList[ids] = [cx, cy]
                lbl = results.multi_handedness[0].classification[0].label
                side_of_hand[0] = lbl

            mp_Draw.draw_landmarks(frame, hand_landmarks, mphands.HAND_CONNECTIONS)
            
        # Calcule le centre de la main
        # on considere les points 2 et 17 de la main car leur milieu donne environ le centre de la main
        middle = [(lmList[2][0] + lmList[17][0])/2, (lmList[2][1] + lmList[17][1])/2] 
            
                
    
        # count the number of raised fingers       
        if len(lmList) != 0:
            fingers_raised = []
            if side_of_hand[0] == 'Left' : # si c'est la main gauche
                        
                # Thumb
                if lmList[tipIds[0]][0] > lmList[tipIds[0] - 1][0]:
                    fingers_raised.append(1)
                else:
                    fingers_raised.append(0)

                # 4 Fingers
                for id in range(1, 5):
                    if lmList[tipIds[id]][1] < lmList[tipIds[id] - 2][1]:
                        fingers_raised.append(1)
                    else:
                        fingers_raised.append(0)

            elif side_of_hand[0] == 'Right' : # si c'est la main droite
                        
                # Thumb
                if lmList[tipIds[0]][0] < lmList[tipIds[0] - 1][0]:
                    fingers_raised.append(1)
                else:
                    fingers_raised.append(0)

                # 4 Fingers
                for id in range(1, 5):
                    if lmList[tipIds[id]][1] < lmList[tipIds[id] - 2][1]:
                        fingers_raised.append(1)
                    else:
                        fingers_raised.append(0)
                                
            totalFingers = fingers_raised.count(1)
            print(totalFingers)
            
    
    cv.imshow('Handtracker',frame)

    """
    if "main en position poing":
        "placer item dans case correspondante"
    """
    """
        # la condition devient alors :
    
        if i<x[0]<(i+1)*width/3 and j<x[1]<(j+1)*height/3 : # cette ligne veut dire si tous les points de la main sont dans une meme zone
                    play_area = [[i*width/3 , (i+1)*width/3] , [j*height/3 , (j+1)*height/3]] # alors cette zone la est consideree comme la zone de jeu
                    if totalFingers == 0 : # car on a choisi le poing comme mouvement pour l'instant
                        a = 2 # play(play_area)         # cest juste pour pas que le programme plante que jai ecrit ca
"""

    # la condition devient alors :
    if totalFingers == 0 : # car on a choisi le poing comme mouvement
        for i in range (3):
            for j in range (3):
                if i*width/3<middle[0]<(i+1)*width/3 and j*height/3<middle[1]<(j+1)*height/3: 
                    top_left = (int(i*width/3),int(j*height/3))
                    # bottom_right = (int((i+1)*width/3),int((j+1)*height/3))
                    frame_new = highlight_cell(frame, top_left[0], top_left[1], int(width/3), int(height/3))
                    cv.imshow('Handtracker',frame_new)

    else :
        cv.imshow('Handtracker',frame)

    # cv.imshow('Frame',frame)
    cv.waitKey(1)
    time.sleep(1/framerate)

    if cv.waitKey(10) == 27:
        break

