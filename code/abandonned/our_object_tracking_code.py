

# S'inspirer du code 'objec_tracking' mais mettre une autre condition pour l'arrêt de l'object tracking (ici la condition c'est d'appuyer sur la touche échap)
# En plus de ça, il ne faut pas que ça détecte les objets oranges mais que ça détecte les mains et les différentes positions dans laquelle elle peut se trouver
# CAD main normale ouverte) et poing (main fermée) et ça doit détecter des mains de toutes les couleurs de peau et même de toutes les couleurs et textures je me dis car ça serait stylé si ça marche même quand on porte un gant. Et ça doit marcher aussi si on a que 4 doigts ou même moins.


# Alors j'arrive pas à importer mediapipe ça me clc
# Ca me dit que ya un pb au niveau de cv2 et de mediapipe ca me clc ptn


import cv2 as cv
import mediapipe as mp
import numpy as np
# import numpy as np
# from ultralytics import YOLO

# load yolov8 model
# model = YOLO('yolov8n.py')
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

# get video frames
cam = cv.VideoCapture(0)
hands = mphands.Hands()

# read frames
while(True):
    ret,image = cam.read()
    image = cv.flip(image,1)

    # Smoothen the image
    image = cv.GaussianBlur(image,(7,7),0)

    # detect objects and track objects
    results = hands.process(image, persist=True)
    # plot results
    image = results[0].plot()
    # visualize
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mphands.HAND_CONNECTIONS)
    cv.imshow('Handtracker',image)
    if "main en position poing":
        "placer item dans case correspondante"
    if cv.waitKey(10) == 27:
        break

cam.release()
cv.destroyAllWindows()

# TO DO LIST

# 1 - réussir à installer mediapipe OKKKKKKKKKK
# 1bis - faire marcher code juste pour détecter main (juste hand tracking et pas que ça détecte main fermée)
# 2 - mettre le feature que ça détecte la main fermée et surtout que ça comprenne que alors ça doit faire qqch (exécuter une commande)
# 3 - séparer la caméra en 9 zones (voir code "based_mouse")
# 4 - faire en sorte que ça joue une case quand poing détecté

# ENSUITE UNE FOIS QUE CA C'EST FAIT, DETECTER LES COULEURS ET LES FORMES ET CODER POUR LE DESIGN D'UN BRACELET NOIR AVEC POINT BLANC.





# 3 - séparer la caméra en 9 zones (voir code "based_mouse")

import cv2 as cv
import mediapipe as mp
import numpy as np

# get video frames
cam = cv.VideoCapture(0)

lower_orange = np.array([5,100,100]) # potentiellement remplacer ça par noir et blanc si on suit l'idee du wristband
upper_orange = np.array([15,255,255])

# read frames
while(True):
    ret,image = cam.read()
    image = cv.flip(image,1)

    # Smoothen the image
    image = cv.GaussianBlur(image,(7,7),0)

    #Define ROI
    mask = np.zeros_like(image)
    mask[100:350,100:350] = [255,255,255]  # Si je veux modifier taille quadrillage, je dois modifier les 5 lignes de 'cv...' et cette ligne là.
    image_roi = cv.bitwise_and(image,mask)
    cv.rectangle(image,(50,50),(350,350),(0,0,255),2)
    cv.line(image,(150,50),(150,350),(0,0,255),1)
    cv.line(image,(250,50),(250,350),(0,0,255),1)
    cv.line(image,(50,150),(350,150),(0,0,255),1)
    cv.line(image,(50,250),(350,250),(0,0,255),1)

    # Threshold
    image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    image_threshold = cv.inRange(image_hsv,lower_orange,upper_orange)

    # Find contours
    contours,hierarchy = cv.findContours(image_threshold,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)

    # Find the index of the largest contour
    if(len(contours)!=0):
        area = [cv.contourArea(c) for c in contours]
        max_index = np.argmax(area)
        cnt = contours[max_index]
        x,y,w,h = cv.boundingRect(cnt)
        cv.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

    # plot results
    # image = results[0].plot()

    # plot results
    cv.imshow('Frame', image)

    # if "main en position poing":
        # "placer item dans case correspondante"
    
    if cv.waitKey(10) == 27:
        break

cam.release()
cv.destroyAllWindows()

# Edward m'a dit qu'il a testé ce code et qu'il marche, il a juste des cases trop petites qui ne prennent pas toute la fenêtre
# Donc juste modiifier la taille des matrices et voir si c'est ok.




# 4 - faire en sorte que ça joue une case quand condition vérifiée (à voir si on choisit poing détecté) 
# OKKKKKKKKK

condition = '' # C'est la condition que doit vérifier l'object tracking pour que le jeu joue un coup.
zone = '' # C'est la zone de la caméra où la condition est réalisée.
            # Donc la variable 'zone' doit contenir 'condition' qlq part

# if condition: # condition doit être un booléen
#    Jouer(zone) # Apparemment cette partie là c'est Manon, moi je lui donne juste la zone que le joueur a choisi car la condition pour que la case soit chosie a été vérifiée.


""" rdv meeting tuteur :
    penser au langage des signes
    se mettre d'accord sur quoi tracker en object tracking
    pb d'éclairage avec l'object-tracking mais ça sera le cas avec tous les types de tracking
    mettre mes codes sur le gitlab (voir comment faire déjà)
    dans un 1er temps sans se poser de questions de consommation d'énergie et d'utilisation du processeur
    Ensuite voir à quel point notre code consomme et utilise l'OS (le processeur)
    Utiliser 'top' ou 'Xload' pour savoir ça
    Regarder sur Aliexpress pour un embout que tu mets en usb et qui donne la consommation (askip ça que 15 euros, cher quoi)
    et enfin améliorer le code pour qu'il soit plus efficace 
    le tuteur veut un mail qui récapitule nos avancées communes et individuelles CHAQUE SEMAINE
    On le revoit le jeudi 27 mars à 12h
"""

# Donc : conseil de Lilian :
# Je peux faire plusieurs fichiers de code et avoir un code principal qui appelle mes autres codes en les important comme si j'importais des librairies
# Ca évite d'avoir un code énorme qui serait la fusion de tous mes fichiers de code
# Ex : si mon fichier s'appelle "camera", alors je ferai "import camera" et quand je voudrais utiliser une fonction de ce fichier je devrais faire :
# "camera.nom_de_fonction" . Donc il faut que j'ai une/des fonction(s) dans mon code et pas juste un bloc d'instructions.



# TO DO LIST :

# 1 - Faire marcher code de Lilian (cam_main_qui_fait_souris) (le code est déjà censé marcher)
# 2 - Implémenter le hand tracking (déjà implémenté dans code de Lilian) OKKKKKK
# 2a - Que ça détecte la main (OKKKKKK)(Voir si je peux améliorer)
# 2b - Que ça dessine des traits sur la main que ça track (Faire ça le 15 mars)
# 3 - Que ça détecte quand la main est en position spéciale (sûrement poing fermé)


# # 2b - Que ça dessine des traits sur la main que ça track (Faire ça le 15 mars)

# Maintenant qu’on a la vidéo, on va créer l’objet hands qui nous permettra de détecter la main droite et gauche ##
# sur la vidéo ainsi que de récupérer les différents coordonnées de ces derniers.
mpHands = mp.solutions.hands

# On crée aussi l’objet drawing_utils que nous utiliserons pour pouvoir 
# tracer des lignes représentant la forme de la main sur celles détectés sur chaque frame de la vidéo
mpDraw = mp.solutions.drawing_utils

# Ensuite nous créons l’objet Hands
Hands = mpHands.Hands()

#Traçage des lignes (Ca va dans la boucle true)
result = Hands.process(image) #Détecte la mains et récupère ces coordonnés
for handLms in result.multi_hand_landmarks:
    for id,lm in enumerate(handLms.landmark):
        h, w, c = image.shape
        cx, cy = int(lm.x*w), int(lm.y*h)
#Dessine un grand cercle
if (id == 0):
    cv.circle(image, (cx, cy), 25, (255, 0, 255), cv.FILLED)
mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)