import cv2
import numpy as np
from pynput.mouse import Controller as MouseController


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

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Inverser l'image horizontalement pour que le mouvement de la main corresponde à celui de la souris
    frame = cv2.flip(frame, 1)
    
    # Appliquer la fonction de détection et de suivi de la main
    detect_and_track_hand(frame)
    
    # Quitter la boucle si la touche 'q' est enfoncée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la capture vidéo et détruire toutes les fenêtres OpenCV
cap.release()
cv2.destroyAllWindows()
