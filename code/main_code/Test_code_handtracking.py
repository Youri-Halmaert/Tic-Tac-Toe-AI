from picamera2 import Picamera2
import cv2 as cv
import mediapipe as mp
import numpy as np
import time

# we also create the object drawing_utils that will be used for the creation of lines to draw on the detected hand on every frame of the video
mp_Draw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

mphands = mp.solutions.hands

width = 735 
height = 735
nb_fingers = 0

# get video frames
cam = Picamera2()
config = cam.create_preview_configuration({"size":(width,height)})
cam.configure(config)
cam.start()

framerate = 30

# then we create the object Hands
Hands = mphands.Hands()

# a bunch of useful lists
lmList = [[0,0]] * 21
tipIds = [4, 8, 12, 16, 20]
side_of_hand = [0]

totalFingers = 0
color = (0,0,0)
middle = [0, 0]
darkmode = False

HEIGHT = 75
WIDTH = 75
MARGIN = 5
playablex = MARGIN
playabley = MARGIN
playsizex = (3*WIDTH + 4*MARGIN)*3
playsizey = (3*HEIGHT + 4*MARGIN)*3
playrect = [playablex,playabley,playsizex,playsizex]

# the function that enables to highlight the chosen cell
def highlight_cell(frame, x, y, w, h, color, alpha):
    overlay = frame.copy()
    cv.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    return cv.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

# the function that enables the user to choose the number of raised fingers we want for the selection of the cell we will play in
'''def choose_number():
    while True:
        try:
            # Ask the user to input a number between 0 and 4
            number = int(input("Please choose a number between 0 and 4: "))
            
            # Check if the number is within the valid range
            if 0 <= number <= 4:
                print(f"You have chosen the number: {number}")
                return number
            else:
                print("The number is not within the range of 0 to 4. Please try again.")
        except ValueError:
            # Handle the case where the input is not a valid integer
            print("Invalid input. Please enter a valid number between 0 and 4.")'''

def handtracking(playrect, pos, clic, nb_fingers):
    # Call the function and store the result in a variable
    #chosen_number = choose_number() #replaced with nb_fingers

    while True:
        frame = cam.capture_array()
        frame = frame[:, :, :3]
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        
        
        #set the color
        if darkmode == False: # if we are in light mode
            color = (234,217,153) # in BGR
        else: # if we are in dark mode
            color = (107,39,42)    # in BGR
        
        # Flips the image the camera returns for a more intuitive experience for the user.
        frame = cv.flip(frame, 1)
        
        frame_new = frame
        # detect the hand and gets its coordinates
        results = Hands.process(frame)
        
        # visualize
        if results.multi_hand_landmarks:
            
            for hand_landmarks in results.multi_hand_landmarks:
                # Here is how we get the coordinates of the hand.
                for ids, landmark in enumerate(hand_landmarks.landmark):
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    lmList[ids] = [cx, cy]
                    lbl = results.multi_handedness[0].classification[0].label
                    side_of_hand[0] = lbl

                mp_Draw.draw_landmarks(frame_new, hand_landmarks, mphands.HAND_CONNECTIONS)
                
            # derivate the coordinates of the middle of the hand
            # we consider the points 2 and 17 of the hand because the center of these 2 points approximately gives the center of the hand
            middle = [(lmList[2][0] + lmList[17][0]) / 2, (lmList[2][1] + lmList[17][1]) / 2] 
        
            # count the number of raised fingers       
            if len(lmList) != 0:
                fingers_raised = []
                # the condition for checking if the thumb is closed or not changes for the left and right hands
                if side_of_hand[0] == 'Left':  # if it's the left hand
                    # Thumb
                    if lmList[tipIds[0]][0] > lmList[tipIds[0] - 1][0]: # we check if the x coordinate of the point representing the tip of the thub is greater than the one before it
                        fingers_raised.append(1)
                    else:
                        fingers_raised.append(0)

                    # 4 Fingers
                    for id in range(1, 5):
                        if lmList[tipIds[id]][1] < lmList[tipIds[id] - 2][1]: # same idea but for the y coordinate
                            fingers_raised.append(1)
                        else:
                            fingers_raised.append(0)

                elif side_of_hand[0] == 'Right':  # if it's the right hand
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
                
            # highlight the cell the user has chosen to play in
            if totalFingers == nb_fingers:
                clic = True
                for i in range(9):
                    for j in range(9):
                        if i * width / 9 < middle[0] < (i + 1) * width / 9 and j * height / 9 < middle[1] < (j + 1) * height / 9:
                            top_left = (int(i * width / 3), int(j * height / 3))
                            frame_new = highlight_cell(frame, top_left[0], top_left[1], int(width / 9), int(height / 9), color, 0.4)
                break
            
            pos = middle
            if clic :
                break
        
        # the creation of lines on the frames to represent the cells of the game
        x = (round(0.33 * width), round(0.33 * height))
        y = (round(0.66 * width), round(0.66 * height))
        
        x11 = (round(0.11 * width), round(0.11 * height))
        x22 = (round(0.22 * width), round(0.22 * height))
        x44 = (round(0.44 * width), round(0.44 * height))
        x55 = (round(0.55 * width), round(0.55 * height))
        x77 = (round(0.77 * width), round(0.77 * height))
        x88 = (round(0.88 * width), round(0.88 * height))
        
        
        cv.line(frame_new, (x[0], 0), (x[0], height), color, 3)
        cv.line(frame_new, (y[0], 0), (y[0], height), color, 3)
        cv.line(frame_new, (0, x[1]), (width, x[1]), color, 3)
        cv.line(frame_new, (0, y[1]), (width, y[1]), color, 3)
        
        cv.line(frame_new, (x11[0], 0), (x11[0], height), color, 1)
        cv.line(frame_new, (x22[0], 0), (x22[0], height), color, 1)
        cv.line(frame_new, (x44[0], 0), (x44[0], height), color, 1)
        cv.line(frame_new, (x55[0], 0), (x55[0], height), color, 1)
        cv.line(frame_new, (x77[0], 0), (x77[0], height), color, 1)
        cv.line(frame_new, (x88[0], 0), (x88[0], height), color, 1)
        cv.line(frame_new, (0, x11[1]), (width, x11[1]), color, 1)
        cv.line(frame_new, (0, x22[1]), (width, x22[1]), color, 1)
        cv.line(frame_new, (0, x44[1]), (width, x44[1]), color, 1)
        cv.line(frame_new, (0, x55[1]), (width, x55[1]), color, 1)
        cv.line(frame_new, (0, x77[1]), (width, x77[1]), color, 1)
        cv.line(frame_new, (0, x88[1]), (width, x88[1]), color, 1)
        
        frame_new = highlight_cell(frame_new, int(playrect[0]),int(playrect[1]), int(playrect[2]), int(playrect[3]),(0,255,0), 0.13) # highlights the area the user has to play in green
        
        cv.imshow('Handtracker', frame_new)
        if cv.waitKey(1) == 27:
            break
        time.sleep(1 / framerate)

    cv.destroyAllWindows()

    return (pos,clic)

#handtracking() # allows to test the code
