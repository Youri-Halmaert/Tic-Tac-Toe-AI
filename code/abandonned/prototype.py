import pygame
import time 

theme = 'driftveil_city.mp3'
sprite_theme = 'undertale_menu.mp3'

darkmode = "n"
if "y" in darkmode:
    BLACK = (255, 255, 255)
    WHITE = (0, 0, 0)
    GREEN = (255, 0, 255)
    RED = (0, 255, 255)
    BLUE = (255,255,0)
else:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0,255,0)

#settings 
sound_on = True #Is the music on? 
#full = False #Are we in full screen? 
sound = "boom.wav"


#player sprites 
cherry = 'cherry.png'
heart = 'heart.png'
red_circle = 'red_circle.png'
blue_cross = 'blue_cross.png'
taby_cat = 'taby_cat.png'

img_p1 = blue_cross
img_p2 = red_circle

amtrow =9
amtcol =9
 # HEIGHT AND WIDTH NEED TO BE LARGER THAN MARGIN !!!
HEIGHT = 75
WIDTH = 75
MARGIN = 5
playcolour = [25, 250, 100]
grid = []
TotalGrid = []
totxsize = ((WIDTH + MARGIN) * amtrow)+5*MARGIN
totysize = ((HEIGHT + MARGIN) * amtcol)+5*MARGIN
    


def ResizePlayBox(playrect,allowedx,allowedy):
    if allowedx == -1 and allowedy == -1:
        playrect[0] = MARGIN
        playrect[1] = MARGIN
        playrect[2] = (3*WIDTH + 4*MARGIN)*3
        playrect[3] = (3*HEIGHT + 4*MARGIN)*3
    else:

        playrect[1]=allowedy*(MARGIN+HEIGHT) + 2*MARGIN + ((allowedy//3 -1)*MARGIN)
        playrect[0]=allowedx*(MARGIN+WIDTH) + 2*MARGIN + ((allowedx//3 -1) *MARGIN)
        playrect[2]=(MARGIN+WIDTH)*3 + MARGIN
        playrect[3]=(MARGIN+HEIGHT)*3 + MARGIN


def NextBox(Ccords,TotalGrid):
    boxFull = False
    if TotalGrid[Ccords[0]%3][Ccords[1]%3] != 0:
        return (-1,-1)
    else:
        return((Ccords[0]%3)*3,(Ccords[1]%3)*3)
def SetWin(Grid,Team,TotalGrid):
    for x in range(amtrow):
        for y in range(amtcol):
            Grid[x][y] = Team
    for x in TotalGrid:
        for y in x:
            y = Team

def winSetter(OC,Team,Grid,TotalGrid):
    TotalGrid[OC[0]//3][OC[1]//3] = Team
    for x in range((OC[0]//3) * 3,(OC[0]//3) *3 + 3):
        for y in range((OC[1]//3) * 3,(OC[1]//3) *3 + 3):
            grid[x][y] = Team
    for x in range(0,3):
        if TotalGrid[x][0] == Team and TotalGrid[x][1] == Team and TotalGrid[x][2] == Team:
            print("Win detected on",x)
            if Team == 1:
                SetWin(Grid,1,TotalGrid)
            else:
                SetWin(Grid,2,TotalGrid)
    for y in range(0,3):
        if TotalGrid[0][y] == Team and TotalGrid[1][y] == Team and TotalGrid[2][y] == Team:
            print("Win detected on ",y)
            if Team == 1:
                SetWin(Grid,1,TotalGrid)
            else:
                SetWin(Grid,2,TotalGrid)
    if (TotalGrid[0][0] ==Team and TotalGrid[1][1] == Team and TotalGrid[2][2] == Team) or (TotalGrid[2][0] == Team and TotalGrid[1][1] == Team and TotalGrid[0][2] == Team ):
        print("Win here detected")
        if Team == 1:
            SetWin(Grid,1,TotalGrid)
        else:
            SetWin(Grid,2,TotalGrid)
    print(TotalGrid)

def winCalc(OuterCords,Grid,TotalGrid):
    OC = OuterCords
    IC = (OC[0]%3,OC[1]%3)
    thisTileTeam = Grid[OC[0]][OC[1]]
    Team = thisTileTeam
    if thisTileTeam == 0:
        return "Invalid Team"
    if IC == (0,0):

        if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]+2][OC[1]] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]+2] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]+1][OC[1]+1] == thisTileTeam and Grid[OC[0]+2][OC[1]+2] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
    elif IC == (1,0):
        if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]-1][OC[1]] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]+2] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
    elif IC == (2,0):
        if Grid[OC[0]-1][OC[1]] == thisTileTeam and Grid[OC[0]-2][OC[1]] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]+2] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]-1][OC[1]+1] == thisTileTeam and Grid[OC[0]-2][OC[1]+2] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
    elif IC == (0,1):
        if Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]-1] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]+2][OC[1]] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
    elif IC == (1,1):
        if Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]-1] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]-1][OC[1]] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]-1][OC[1]-1] == thisTileTeam and Grid[OC[0]+1][OC[1]+1] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]-1][OC[1]+1] == thisTileTeam and Grid[OC[0]+1][OC[1]-1] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)

    elif IC == (2,1):
        if Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]-1] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]-1][OC[1]] == thisTileTeam and Grid[OC[0]-2][OC[1]] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)

    elif IC == (0,2):
        if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]+2][OC[1]] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]][OC[1]-1] == thisTileTeam and Grid[OC[0]][OC[1]-2] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]+1][OC[1]-1] == thisTileTeam and Grid[OC[0]+2][OC[1]-2] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
    elif IC == (1,2):
        if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]-1][OC[1]] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]][OC[1]-1] == thisTileTeam and Grid[OC[0]][OC[1]-2] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)

    elif IC == (2,2):
        if (Grid[OC[0]][OC[1]-1] == thisTileTeam and Grid[OC[0]][OC[1]-2] == thisTileTeam) :
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif (Grid[OC[0]-1][OC[1]] == thisTileTeam and Grid[OC[0]-2][OC[1]] == thisTileTeam):
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
        elif Grid[OC[0]-1][OC[1]-1] == thisTileTeam and Grid[OC[0]-2][OC[1]-2] == thisTileTeam:
            winSetter(OC,thisTileTeam,Grid,TotalGrid)
    amtused = 0
    #print(OC[0],IC[0],OC[1],IC[1])
    for x in range(OC[0]-IC[0],OC[0]-IC[0]+3):
        for y in range(OC[1]-IC[1],OC[1]-IC[1]+3):
            if Grid[x][y] != 0:
                amtused = amtused + 1
    if amtused == 9:
        if TotalGrid[OC[0]//3][OC[1]//3] == 0:
            TotalGrid[OC[0]//3][OC[1]//3] = -1
            print("Box tied!!")
    #print(TiedBox)   
        

def menu():
    """Main menu of the game"""
    global sound_on
    global game
    global done
    global in_menu
    
    #make the button hitboxes
    pvp_start = pygame.Rect(327.5, 375, 90, 30)
    pygame.draw.rect(screen, [0,0,0], pvp_start) 
    
    sound_hitbox = pygame.Rect(709, 709, 26, 26)
    pygame.draw.rect(screen, [0,0,0], sound_hitbox) 
    
    #fullscreen_hitbox = pygame.Rect(709, 10, 26, 26)
    #pygame.draw.rect(screen, [0,0,0], fullscreen_hitbox) 
    
    sprite_selection_hitbox = pygame.Rect(327.5, 300, 90, 30)
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox) 
    
    #make the background appear 
    t_anim = int(time.time()*10)
    if t_anim%10<5: 
        menu_image = pygame.image.load('menu_anim.png')
    else:
        menu_image = pygame.image.load('menu.png')
    screen.blit(menu_image,(0,0))
    
    #hourglass test 
    if t_anim%20 == 0: 
        hourglass_img = pygame.image.load('hourglass0.png')
    elif t_anim%20 < 6: 
        hourglass_img = pygame.image.load('hourglass1.png')
    elif t_anim%20 < 10: 
        hourglass_img = pygame.image.load('hourglass2.png')
    elif t_anim%20 < 14: 
        hourglass_img = pygame.image.load('hourglass3.png')
    elif t_anim%20 < 16: 
        hourglass_img = pygame.image.load('hourglass4.png')
    elif t_anim%20 < 18: 
        hourglass_img = pygame.image.load('hourglass5.png')
    else:
        hourglass_img = pygame.image.load('hourglass6.png')
    screen.blit(hourglass_img,(0,0))
    
    #make the buttons appear 
    pos = pygame.mouse.get_pos()
    if pvp_start.collidepoint(pos):
        pvp_start_img = pygame.image.load('start_hover.png')
    else : 
        pvp_start_img = pygame.image.load('start.png')
    screen.blit(pvp_start_img, (327.5, 375)) 
    
    if sprite_selection_hitbox.collidepoint(pos):
        sprites_img = pygame.image.load('sprite_select_hover.png')
    else : 
        sprites_img = pygame.image.load('sprite_select.png')
    screen.blit(sprites_img, (327.5, 300))
    
    if sound_hitbox.collidepoint(pos):
        sound_button = pygame.image.load('sound_'+('on' if sound_on else 'off')+'_selected.png')
    else : 
        sound_button = pygame.image.load('sound_'+('on' if sound_on else 'off')+'.png')
    screen.blit(sound_button, (709, 709))
    
    #if fullscreen_hitbox.collidepoint(pos):
        #fullscreen_img = pygame.image.load('fullscreen_selected.png')
    #else : 
        #fullscreen_img = pygame.image.load('fullscreen.png')
    #screen.blit(fullscreen_img, (709, 10))
    
    
    #handle events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            game = True
        elif event.type == pygame.K_q:
            print ("hiii")
            done = True
            game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #buttons clicked -> consequences
            #collide in button creation (rectangle creation) to change appearance 
            if pvp_start.collidepoint(pos):
                game = True
                if sound_on : 
                    pygame.mixer.music.load(sound)
                    pygame.mixer.music.play()
                
            
            if sprite_selection_hitbox.collidepoint(pos):
                in_menu = False
                if sound_on : 
                    pygame.mixer.music.load(sprite_theme)
                    pygame.mixer.music.play()
                    
            
            if sound_hitbox.collidepoint(pos):
                if sound_on : 
                    pygame.mixer.music.stop()
                    sound_on = False 
                else : 
                    sound_on = True
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play()
                    
            #if fullscreen_hitbox.collidepoint(pos): 
                #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    clock.tick(60)
        
    pygame.display.flip()




def sprite_menu():
    """Menu for the sprite selection"""
    global sound_on 
    global done 
    global in_menu 
    global img_p1 
    global img_p2 
    global game
    
    
    #make the button hitboxes
    menu_hitbox = pygame.Rect(327.5, 10, 90, 30)
    pygame.draw.rect(screen, [0,0,0], menu_hitbox) 
    
    sound_hitbox = pygame.Rect(709, 709, 26, 26)
    pygame.draw.rect(screen, [0,0,0], sound_hitbox) 
    
    #sprite hitboxes
    #left
    sprite_selection_hitbox1l = pygame.Rect(150, 150, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox1l) 
    
    sprite_selection_hitbox2l = pygame.Rect(150, 250, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox2l) 
    
    sprite_selection_hitbox3l = pygame.Rect(150, 350, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox3l) 
    
    sprite_selection_hitbox4l = pygame.Rect(150, 450, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox4l) 
    
    sprite_selection_hitbox5l = pygame.Rect(150, 550, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox5l) 
    
    l_hitboxes = [sprite_selection_hitbox1l, sprite_selection_hitbox2l, sprite_selection_hitbox3l, sprite_selection_hitbox4l, sprite_selection_hitbox5l]
    
    #right
    sprite_selection_hitbox1r = pygame.Rect(510, 150, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox1r) 
    
    sprite_selection_hitbox2r = pygame.Rect(510, 250, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox2r) 
    
    sprite_selection_hitbox3r = pygame.Rect(510, 350, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox3r) 
    
    sprite_selection_hitbox4r = pygame.Rect(510, 450, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox4r) 
    
    sprite_selection_hitbox5r = pygame.Rect(510, 550, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox5r) 
    
    r_hitboxes = [sprite_selection_hitbox1r, sprite_selection_hitbox2r, sprite_selection_hitbox3r, sprite_selection_hitbox4r, sprite_selection_hitbox5r]
    
    #make the background appear 
    background = pygame.image.load('sprite_menu.png')
    screen.blit(background,(0,0))
    
    #make the buttons appear 
    pos = pygame.mouse.get_pos()
    if menu_hitbox.collidepoint(pos):
        menu_img = pygame.image.load('go_menu_hover.png')
    else : 
        menu_img = pygame.image.load('go_menu.png')
    screen.blit(menu_img, (327.5, 10)) 
    
    if sound_hitbox.collidepoint(pos):
        sound_button = pygame.image.load('sound_'+('on' if sound_on else 'off')+'_selected.png')
    else : 
        sound_button = pygame.image.load('sound_'+('on' if sound_on else 'off')+'.png')
    screen.blit(sound_button, (709, 709))
    
    #show the current selected sprites 
    left_selected = pygame.image.load(img_p1)
    right_selected = pygame.image.load(img_p2)
    screen.blit(left_selected, (10, 375)) 
    screen.blit(right_selected, (660, 375)) 
    
    #show the other sprite options 
    t_anim = int(time.time()*10)
    sprite_options = [cherry, heart, red_circle, blue_cross, taby_cat] #all options
    for i in range(len(sprite_options)):
        if ((img_p1 == sprite_options[i]) or (img_p2 == sprite_options[i])): #if the sprite is already selected
            screen.blit(pygame.image.load("lock.png"), (150, 150+i*100))
            screen.blit(pygame.image.load("lock.png"), (510, 150+i*100))
        else:
            if l_hitboxes[i].collidepoint(pos): #if hovered
                if t_anim%10<5:
                    screen.blit(pygame.image.load(sprite_options[i][:-4]+'_run.png'), (150, 150+i*100)) #left
                else:
                    screen.blit(pygame.image.load(sprite_options[i]), (150, 150+i*100)) #left
                screen.blit(pygame.image.load(sprite_options[i]), (510, 150+i*100)) #right  
            elif r_hitboxes[i].collidepoint(pos):
                if t_anim%10<5:
                    screen.blit(pygame.image.load(sprite_options[i][:-4]+'_run.png'), (510, 150+i*100)) #right
                else:
                    screen.blit(pygame.image.load(sprite_options[i]), (510, 150+i*100)) #right
                screen.blit(pygame.image.load(sprite_options[i]), (150, 150+i*100)) #left
            
            else:
                screen.blit(pygame.image.load(sprite_options[i]), (510, 150+i*100)) #right
                screen.blit(pygame.image.load(sprite_options[i]), (150, 150+i*100)) #left
         
            
         
            
    #kitty test:
    if t_anim%2 == 1:
        cat_run = pygame.image.load('taby_cat.png')
    else:
        cat_run = pygame.image.load('taby_cat_run.png')
    i+=1
    screen.blit(cat_run,(745-10*(t_anim%200), 650))
    
    
    
    
    #handle events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            game = True
        elif event.type == pygame.K_q:
            print ("hiii")
            done = True
            game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #buttons clicked -> consequences
            #collide in button creation (rectangle creation) to change appearance 
            #left
            if (sprite_selection_hitbox1l.collidepoint(pos) and ((img_p1 != cherry) and (img_p2 != cherry))): #if click on a sprite for a player and it isn't already selected
                img_p1 = cherry
            
            if (sprite_selection_hitbox2l.collidepoint(pos) and ((img_p1 != heart) and (img_p2 != heart))): 
                img_p1 = heart

            if (sprite_selection_hitbox3l.collidepoint(pos) and ((img_p1 != red_circle) and (img_p2 != red_circle))): 
                img_p1 = red_circle
                
            if (sprite_selection_hitbox4l.collidepoint(pos) and ((img_p1 != blue_cross) and (img_p2 != blue_cross))): 
                img_p1 = blue_cross
            
            if (sprite_selection_hitbox5l.collidepoint(pos) and ((img_p1 != taby_cat) and (img_p2 != taby_cat))): 
                img_p1 = taby_cat
            
            #right
            if (sprite_selection_hitbox1r.collidepoint(pos) and ((img_p1 != cherry) and (img_p2 != cherry))): #if click on a sprite for a player and it isn't already selected
                img_p2 = cherry
            
            if (sprite_selection_hitbox2r.collidepoint(pos) and ((img_p1 != heart) and (img_p2 != heart))): 
                img_p2 = heart

            if (sprite_selection_hitbox3r.collidepoint(pos) and ((img_p1 != red_circle) and (img_p2 != red_circle))): 
                img_p2 = red_circle
                
            if (sprite_selection_hitbox4r.collidepoint(pos) and ((img_p1 != blue_cross) and (img_p2 != blue_cross))): 
                img_p2 = blue_cross
            
            if (sprite_selection_hitbox5r.collidepoint(pos) and ((img_p1 != taby_cat) and (img_p2 != taby_cat))): 
                img_p2 = taby_cat
            
            if sound_hitbox.collidepoint(pos):
                if sound_on : 
                    pygame.mixer.music.stop()
                    sound_on = False 
                else : 
                    sound_on = True
                    pygame.mixer.music.load(sprite_theme)
                    pygame.mixer.music.play()
            
            if menu_hitbox.collidepoint(pos):
                if sound_on: 
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play()
                in_menu = True
    
    clock.tick(60)
        
    pygame.display.flip()





for row in range(3):

    TotalGrid.append([])
    for column in range(3):
        TotalGrid[row].append(0)



for row in range(amtrow):

    grid.append([])
    for column in range(amtcol):
        grid[row].append(0)


print(grid)
# Initialize pygame
pygame.init()

WINDOW_SIZE = [totxsize, totysize]
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Ulimate Tic tac toe")
try:
    gameIcon = pygame.image.load('Logo2.png')
    pygame.display.set_icon(gameIcon)
except:
    print("No logo found starting anyway")
allowedx = -1
allowedy = -1
playablex = MARGIN
playabley = MARGIN
playsizex = (3*WIDTH + 4*MARGIN)*3
playsizey = (3*HEIGHT + 4*MARGIN)*3
playrect = [playablex,playabley,playsizex,playsizex]
playwidth = int(WIDTH//20)
if playwidth == 0:
    playwidth = 1
done = False
redPlaying = True
clock = pygame.time.Clock()
tot3by3 = (3*WIDTH+MARGIN)


in_menu = True
game = False #True if a button to start the game has been clicked 
pygame.mixer.music.load(theme)
pygame.mixer.music.play()



while not game : 
    if in_menu :
        menu()
    else : 
        sprite_menu()
    
while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.K_q:
            print ("hiii")
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            xcord = ((pos[0] - ((pos[0]//tot3by3)-1)*MARGIN) - 2*MARGIN) // (MARGIN+WIDTH)
            ycord = ((pos[1] - ((pos[1]//tot3by3)-1)*MARGIN) - 2*MARGIN)// (MARGIN+HEIGHT)
            print("Click ", pos, "Grid coordinates: ", xcord, ycord , "Inner cords",xcord%3,ycord%3)
            if xcord /8 <= 1 and ycord /8 <= 1:
                if grid[xcord][ycord] == 0:
                    if allowedx == -1 and allowedy == -1: #move anywhere
                        if redPlaying == True:
                            grid[xcord][ycord] = 1
                            redPlaying = False
                            playcolour = BLUE
                        else:
                            grid[xcord][ycord] = 2
                            redPlaying = True
                            playcolour = RED
                        winCalc([xcord,ycord],grid,TotalGrid)
                        allowedx ,allowedy = NextBox([xcord,ycord],TotalGrid)
                        ResizePlayBox(playrect,allowedx,allowedy)
                    elif allowedx <= xcord <= allowedx+2 and allowedy <= ycord <= allowedy+2:
                        if redPlaying == True:
                            grid[xcord][ycord] = 1
                            redPlaying = False
                            playcolour = BLUE
                        else:
                            grid[xcord][ycord] = 2
                            redPlaying = True
                            playcolour = RED
                        winCalc([xcord,ycord],grid,TotalGrid)
                        allowedx ,allowedy = NextBox([xcord,ycord],TotalGrid)
                        ResizePlayBox(playrect,allowedx,allowedy)


    # Set the screen background
    screen.fill(BLACK)
    
    # Draw the grid
    extramarginx = 0
    extramarginy = 0
    for row in range(amtrow):
        if row%3 == 0:
            extramarginy = extramarginy +MARGIN
        for column in range(amtcol):
            w = False #to see if an image needs to be drawn
            if column%3 == 0:
                extramarginx = extramarginx + MARGIN
            pygame.draw.rect(screen, WHITE,[((MARGIN + WIDTH) * column) + MARGIN + extramarginx,((MARGIN + HEIGHT) * row) + MARGIN+ extramarginy,WIDTH,HEIGHT])
            pygame.draw.rect(screen, playcolour, playrect,playwidth)
            if grid[column][row] == 1:
                w = True
                img = pygame.image.load(img_p1)
            if grid[column][row] == 2:
                w = True
                img = pygame.image.load(img_p2)
            if w : 
                screen.blit(img, (((MARGIN + WIDTH) * column) + MARGIN + extramarginx,
                              ((MARGIN + HEIGHT) * row) + MARGIN+ extramarginy))
                
        extramarginx =0

    
    clock.tick(60)
        
    pygame.display.flip()

pygame.quit()







