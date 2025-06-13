# The interface of the game (first version)
import pygame
import time 

theme = 'sounds/menu_percu.wav'
sprite_theme = 'sounds/spriteselect.wav'
start_music = 'sounds/startmenu.wav'
game_music = 'sounds/gamemenu.wav'
settings_music = 'sounds/settingsmenu.wav'
connect_music = 'sounds/connect.wav'
gameover_music = 'sounds/gameover.wav'

darkmode = False

#settings 
sound_on = True #Is the music on? 
sound = "sounds/start.mp3"
cat_is_dog = False #True when the cat is a dog 
game_over = ''
full_cases = 0 #to determine when the game is a tie 
fullscreen = False 
offset = (0, 0) #offsets to place the elements correctly on the screen 
active = 0

#player sprites 
cherry = 'images/cherry.png'
heart = 'images/heart.png'
red_circle = 'images/red_circle.png'
blue_cross = 'images/blue_cross.png'
taby_cat = 'images/taby_cat.png'
bird = 'images/bird.png'

#small chances to be used
dog = 'images/dog.png'


#beginning stuff 
amtrow =9
amtcol =9

# HEIGHT AND WIDTH NEED TO BE LARGER THAN MARGIN !!!
HEIGHT = 75
WIDTH = 75
MARGIN = 5
playcolour = [25, 250, 100]
grid = []
TotalGrid = []
TTG = [[0 for _ in range(9)] for _ in range(9)]
totxsize = ((WIDTH + MARGIN) * amtrow)+5*MARGIN
totysize = ((HEIGHT + MARGIN) * amtcol)+5*MARGIN


for row in range(3):

    TotalGrid.append([])
    for column in range(3):
        TotalGrid[row].append(0)



for row in range(amtrow):

    grid.append([])
    for column in range(amtcol):
        grid[row].append(0)

# Initialize pygame
pygame.init()

WINDOW_SIZE = [totxsize, totysize]
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Super Retro Tic Tac Toe")
try:
    gameIcon = pygame.image.load('images/logo.png')
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
color_inactive = pygame.Color((214,85,79))
color_active = pygame.Color((88,204,112))
color_pseudo = color_inactive
color_ip = color_inactive
color_port = color_inactive
clock = pygame.time.Clock()
tot3by3 = (3*WIDTH+MARGIN)


if (time.time()*1000//2)%7 == 0: 
    taby_cat = dog
    cat_is_dog = True

img_p1 = blue_cross
img_p2 = red_circle

#images to transition between the different menus
transition0 = 'images/transition.png'
transition1= 'images/transition_run.png'



# ----------------------------------------------------- Functions -----------------------------------------------------
def ResizePlayBox(playrect,allowedx,allowedy, HEIGHT, WIDTH, offset):

    #add offset 
    xoff, yoff = offset #see if needed here or somewhere else 

    if allowedx == -1 and allowedy == -1:
        playrect[0] = MARGIN + xoff 
        playrect[1] = MARGIN + yoff 
        playrect[2] = (3*WIDTH + 4*MARGIN)*3 
        playrect[3] = (3*HEIGHT + 4*MARGIN)*3 
    else:

        playrect[1]=allowedy*(MARGIN+HEIGHT) + 2*MARGIN + yoff + ((allowedy//3 -1)*MARGIN) 
        playrect[0]=allowedx*(MARGIN+WIDTH) + 2*MARGIN + xoff + ((allowedx//3 -1) *MARGIN) 
        playrect[2]=(MARGIN+WIDTH)*3 + MARGIN
        playrect[3]=(MARGIN+HEIGHT)*3 + MARGIN


def NextBox(Ccords,TotalGrid):
    if TotalGrid[Ccords[0]%3][Ccords[1]%3] != 0:
        return (-1,-1)
    else:
        return((Ccords[0]%3)*3,(Ccords[1]%3)*3)

def start_menu(done, game, in_menu, screen, fullscreen, offset, nb_fingers, select_mouse):
    """Menu at the start to choose object detection settings and read the rules"""
    global sound_on 
    global img_p1 
    global img_p2 
    global darkmode
    
    xoff, yoff = offset 

    #make the button hitboxes
    exit_hitbox = pygame.Rect(343.5+xoff, 707+yoff, 58, 30)
    pygame.draw.rect(screen, [0,0,0], exit_hitbox) 

    gotit_hitbox = pygame.Rect(340.5+xoff, 500+yoff, 64, 30)
    pygame.draw.rect(screen, [0,0,0], gotit_hitbox) 
    
    sound_hitbox = pygame.Rect(709+xoff, 709+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], sound_hitbox) 
    
    darkmode_hitbox = pygame.Rect(709+xoff, 10+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], darkmode_hitbox)

    fullscreen_hitbox = pygame.Rect(10+xoff, 709+yoff, 28, 28)
    pygame.draw.rect(screen, [0,0,0], fullscreen_hitbox) 

    #object tracking button hitboxes 
    zero_hitbox = pygame.Rect(105+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], zero_hitbox) 

    one_hitbox = pygame.Rect(205+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], one_hitbox) 

    two_hitbox = pygame.Rect(305+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], two_hitbox) 

    three_hitbox = pygame.Rect(405+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], three_hitbox) 

    four_hitbox = pygame.Rect(505+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], four_hitbox) 

    mouse_hitbox = pygame.Rect(605+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], mouse_hitbox) 
                    
    if darkmode: 
        background = 'images/sprite_menu_v2_nuit.png'
    else: 
        background = 'images/sprite_menu_v2.png'
    sprite_background = pygame.image.load(background)
    screen.blit(sprite_background,(0+xoff,0+yoff))
    
    #add text
    font = pygame.font.Font('Minecraft.ttf', 13)

    font_color = (255,255,255) if darkmode else (0,0,0)

    line_1 = font.render(f"Welcome to Super Retro Tic Tac Toe!", True, font_color)
    line_2 = font.render(f"This game is played on a tic-tac-toe board made up of 9 small boards.", True, font_color)
    line_3 = font.render(f"Win 3 small boards in a row (vertical, horizontal or diagonal) to win the game!", True, font_color)
    line_4 = font.render(f"You can only play in the small board placed where the opponent played in their own small board the previous turn.", True, font_color)
    line_5 = font.render(f"To activate hand tracking, click on the mouse button below.", True, font_color)
    line_6 = font.render(f"The number buttons let you choose how many fingers up are the signal to click!", True, font_color)
    line_7 = font.render(f"You can choose your play symbol and if a player is an AI in the sprites menu.", True, font_color)
    line_8 = font.render(f"Have fun!", True, font_color)


    line_1_rect = line_1.get_rect(center=(totxsize//2+xoff, totysize//2 - 280+yoff))
    line_2_rect = line_2.get_rect(center=(totxsize//2+xoff, totysize//2 - 250+yoff))
    line_3_rect = line_3.get_rect(center=(totxsize//2+xoff, totysize//2 - 220+yoff))
    line_4_rect = line_4.get_rect(center=(totxsize//2+xoff, totysize//2 - 190+yoff))
    line_5_rect = line_5.get_rect(center=(totxsize//2+xoff, totysize//2 - 160+yoff))
    line_6_rect = line_6.get_rect(center=(totxsize//2+xoff, totysize//2 - 130+yoff))
    line_7_rect = line_7.get_rect(center=(totxsize//2+xoff, totysize//2 - 100+yoff))
    line_8_rect = line_8.get_rect(center=(totxsize//2+xoff, totysize//2 - 70+yoff))


    screen.blit(line_1, line_1_rect)
    screen.blit(line_2, line_2_rect)
    screen.blit(line_3, line_3_rect)
    screen.blit(line_4, line_4_rect)
    screen.blit(line_5, line_5_rect)
    screen.blit(line_6, line_6_rect)
    screen.blit(line_7, line_7_rect)
    screen.blit(line_8, line_8_rect)

    #define t_anim
    t_anim = int(time.time()*10)
    
    #triggered by random event? 
    #bird test
    if t_anim%2 == 1:
        bird_fly = pygame.image.load(bird)
    else:
        bird_fly = pygame.image.load(bird[:-4]+'2.png')
    screen.blit(bird_fly,(-745+20*(t_anim%500)+xoff, 100+yoff))
    
    
    #kitty test:
    if t_anim%2 == 1:
        cat_run = pygame.image.load(taby_cat)
    else:
        cat_run = pygame.image.load(taby_cat[:-4]+'_run.png')
    screen.blit(cat_run,(745-10*(t_anim%200)+xoff, 650+yoff))



    #make the buttons appear 
    pos = pygame.mouse.get_pos()

    if exit_hitbox.collidepoint(pos):
        exit_img = pygame.image.load('images/exit_hover.png')
    else : 
        exit_img = pygame.image.load('images/exit.png')
    screen.blit(exit_img, (343.5+xoff, 707+yoff)) 

    if gotit_hitbox.collidepoint(pos):
        gotit_img = pygame.image.load('images/got_it_hover.png')
    else : 
        gotit_img = pygame.image.load('images/got_it.png')
    screen.blit(gotit_img, (340.5+xoff, 500+yoff)) 
    
    if sound_hitbox.collidepoint(pos):
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2_selected.png')
    else : 
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2.png')
    screen.blit(sound_button, (709+xoff, 709+yoff))
    
    if darkmode: 
        darkmode_image = 'images/light_mode_v2.png'
    else: 
        darkmode_image = 'images/dark_mode_v2.png'
    if darkmode_hitbox.collidepoint(pos):
        darkmode_image = darkmode_image[:-4]+'_selected.png'
    darkmode_button = pygame.image.load(darkmode_image)
    screen.blit(darkmode_button, (709+xoff, 10+yoff))
    
    fullscreen_img = 'images/fullscreen' +('_on.png' if fullscreen else '.png')
    if fullscreen_hitbox.collidepoint(pos):
        fullscreen_img = fullscreen_img[:-4]+'_selected.png'
    screen.blit(pygame.image.load(fullscreen_img), (10+xoff, 709+yoff))


    #object tracking buttons 
    if nb_fingers == 0:
        zero_image = 'images/zero_clicked.png'
    else:
        zero_image = 'images/zero.png'
    if zero_hitbox.collidepoint(pos):
        zero_image = zero_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(zero_image), (105+xoff, 400+yoff))

    if nb_fingers == 1:
        one_image = 'images/one_clicked.png'
    else:
        one_image = 'images/one.png'
    if one_hitbox.collidepoint(pos):
        one_image = one_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(one_image), (205+xoff, 400+yoff))

    if nb_fingers == 2:
        two_image = 'images/two_clicked.png'
    else:
        two_image = 'images/two.png'
    if two_hitbox.collidepoint(pos):
        two_image = two_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(two_image), (305+xoff, 400+yoff))

    if nb_fingers == 3:
        three_image = 'images/three_clicked.png'
    else:
        three_image = 'images/three.png'
    if three_hitbox.collidepoint(pos):
        three_image = three_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(three_image), (405+xoff, 400+yoff))

    if nb_fingers == 4:
        four_image = 'images/four_clicked.png'
    else:
        four_image = 'images/four.png'
    if four_hitbox.collidepoint(pos):
        four_image = four_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(four_image), (505+xoff, 400+yoff))
    
    if select_mouse:
        mouse_image = 'images/mouse_clicked.png'
    else:
        mouse_image = 'images/mouse.png'
    if mouse_hitbox.collidepoint(pos):
        mouse_image = mouse_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(mouse_image), (605+xoff, 400+yoff))

    #make the background appear 
    if fullscreen: 
        if darkmode:
            background_img = "images/background_nuit.png"
        else:
            background_img = "images/background.png"
        infoObject = pygame.display.Info()
        screen.blit(pygame.image.load(background_img), ((infoObject.current_w - 1920)/2, (infoObject.current_h - 1080)/2))

    #handle events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            game = True
            in_menu = True
        elif event.type == pygame.K_q:
            done = True
            game = True
            in_menu = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #buttons clicked -> consequences

            if exit_hitbox.collidepoint(pos):
                done = True    
                game = True 
                in_menu = True

            #object tracking buttons
            if zero_hitbox.collidepoint(pos):
                nb_fingers = 0

            if one_hitbox.collidepoint(pos):
                nb_fingers = 1
            
            if two_hitbox.collidepoint(pos):
                nb_fingers = 2

            if three_hitbox.collidepoint(pos):
                nb_fingers = 3

            if four_hitbox.collidepoint(pos):
                nb_fingers = 4

            if mouse_hitbox.collidepoint(pos):
                select_mouse = not select_mouse

            if sound_hitbox.collidepoint(pos):
                if sound_on : 
                    pygame.mixer.music.stop()
                    sound_on = False 
                else : 
                    sound_on = True
                    pygame.mixer.music.load(start_music)
                    pygame.mixer.music.play(-1)
            
            if gotit_hitbox.collidepoint(pos):
                kitty_transition(offset, fullscreen, darkmode)
                if sound_on:
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)
                in_menu = True

            
            if darkmode_hitbox.collidepoint(pos): 
                if darkmode: 
                    darkmode = False
                else: 
                    darkmode = True
    
            if fullscreen_hitbox.collidepoint(pos): 
                if fullscreen: 
                    screen = pygame.display.set_mode(WINDOW_SIZE)
                    offset = (0,0)
                else: 
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    infoObject = pygame.display.Info()
                    offset = ((infoObject.current_w-745)/2, (infoObject.current_h-745)/2)
                fullscreen = not fullscreen #becomes False if True, True if False 

    clock.tick(60)
        
    pygame.display.flip()

    return (done, game, in_menu, screen, fullscreen, offset, nb_fingers, select_mouse)


def menu(done, game, in_menu, screen, online, fullscreen, offset): 
    """Main menu of the game"""
    global sound_on
    global darkmode

    xoff, yoff = offset 

    #make the button hitboxes
    exit_hitbox = pygame.Rect(343.5+xoff, 707+yoff, 58, 30)
    pygame.draw.rect(screen, [0,0,0], exit_hitbox) 

    local_start = pygame.Rect(333.5+xoff, 375+yoff, 78, 30)
    pygame.draw.rect(screen, [0,0,0], local_start) 

    online_start = pygame.Rect(333.5+xoff, 450+yoff, 78, 30)
    pygame.draw.rect(screen, [0,0,0], online_start) 
    
    sound_hitbox = pygame.Rect(709+xoff, 709+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], sound_hitbox) 
    
    fullscreen_hitbox = pygame.Rect(10+xoff, 709+yoff, 28, 28)
    pygame.draw.rect(screen, [0,0,0], fullscreen_hitbox) 
    
    sprite_selection_hitbox = pygame.Rect(333.5+xoff, 300+yoff, 78, 30)
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox) 
    
    darkmode_hitbox = pygame.Rect(709+xoff, 10+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], darkmode_hitbox)
    

    t_anim = int(time.time()*10)
    if t_anim%10<5: 
        menu_image = 'images/menu_v2_anim.png'
    else:
        menu_image = 'images/menu_v2.png'
    if darkmode:
        menu_image = menu_image[:-4]+'_nuit.png'
    menu_background = pygame.image.load(menu_image)
    screen.blit(menu_background,(0+xoff,0+yoff))
    
    #make the buttons appear 
    pos = pygame.mouse.get_pos()

    if exit_hitbox.collidepoint(pos):
        exit_img = pygame.image.load('images/exit_hover.png')
    else : 
        exit_img = pygame.image.load('images/exit.png')
    screen.blit(exit_img, (343.5+xoff, 707+yoff)) 

    if local_start.collidepoint(pos):
        local_start_img = pygame.image.load('images/local_hover.png')
    else : 
        local_start_img = pygame.image.load('images/local.png')
    screen.blit(local_start_img, (333.5+xoff, 375+yoff)) 

    if online_start.collidepoint(pos):
        online_start_img = pygame.image.load('images/online_hover.png')
    else : 
        online_start_img = pygame.image.load('images/online.png')
    screen.blit(online_start_img, (333.5+xoff, 450+yoff)) 
    
    if sprite_selection_hitbox.collidepoint(pos):
        sprites_img = pygame.image.load('images/sprite_select_v2_hover.png')
    else : 
        sprites_img = pygame.image.load('images/sprite_select_v2.png')
    screen.blit(sprites_img, (333.5+xoff, 300+yoff))
    
    if darkmode: 
        darkmode_image = 'images/light_mode_v2.png'
    else: 
        darkmode_image = 'images/dark_mode_v2.png'
    if darkmode_hitbox.collidepoint(pos):
        darkmode_image = darkmode_image[:-4]+'_selected.png'
    darkmode_button = pygame.image.load(darkmode_image)
    screen.blit(darkmode_button, (709+xoff, 10+yoff))
    
    
    if sound_hitbox.collidepoint(pos):
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2_selected.png')
    else : 
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2.png')
    screen.blit(sound_button, (709+xoff, 709+yoff))
    
    fullscreen_img = 'images/fullscreen' +('_on.png' if fullscreen else '.png')
    if fullscreen_hitbox.collidepoint(pos):
        fullscreen_img = fullscreen_img[:-4]+'_selected.png'
    screen.blit(pygame.image.load(fullscreen_img), (10+xoff, 709+yoff))

    #make the background appear 
    if fullscreen: 
        if darkmode:
            background_img = "images/background_nuit.png"
        else:
            background_img = "images/background.png"
        infoObject = pygame.display.Info()
        screen.blit(pygame.image.load(background_img), ((infoObject.current_w - 1920)/2, (infoObject.current_h - 1080)/2))

    #handle events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            game = True
        elif event.type == pygame.K_q:
            done = True
            game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #buttons clicked -> consequences
            #collide in button creation (rectangle creation) to change appearance 
            if exit_hitbox.collidepoint(pos):
                done = True    
                game = True 

            if local_start.collidepoint(pos):
                kitty_transition(offset, fullscreen, darkmode)
                game = True
                if sound_on : 
                    pygame.mixer.music.load(game_music)
                    pygame.mixer.music.play(-1)
                
            if online_start.collidepoint(pos):
                kitty_transition(offset, fullscreen, darkmode)
                if sound_on:
                    pygame.mixer.music.load(connect_music)
                    pygame.mixer.music.play(-1)
                online = True
                in_menu = False


            if sprite_selection_hitbox.collidepoint(pos):
                kitty_transition(offset, fullscreen, darkmode)
                in_menu = False
                if sound_on : 
                    pygame.mixer.music.load(sprite_theme)
                    pygame.mixer.music.play(-1)
                    
            
            if sound_hitbox.collidepoint(pos):
                if sound_on : 
                    pygame.mixer.music.stop()
                    sound_on = False 
                else : 
                    sound_on = True
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)
                    
                    
            if darkmode_hitbox.collidepoint(pos): 
                if darkmode: 
                    darkmode = False
                else: 
                    darkmode = True
            
            if fullscreen_hitbox.collidepoint(pos): 
                if fullscreen: 
                    screen = pygame.display.set_mode(WINDOW_SIZE)
                    offset = (0, 0)

                else: 
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    infoObject = pygame.display.Info()
                    offset = ((infoObject.current_w-745)/2, (infoObject.current_h-745)/2)
                fullscreen = not fullscreen #becomes False if True, True if False 

    clock.tick(60)
        
    pygame.display.flip()
    return done, game, in_menu, screen, online, fullscreen, offset


def sprite_menu(done, game, in_menu, screen, fullscreen, offset, gamemodes, difficulty):
    """Menu for the sprite selection"""
    global sound_on 
    global img_p1 
    global img_p2 
    global darkmode
    
    xoff, yoff = offset 

    #make the button hitboxes
    exit_hitbox = pygame.Rect(343.5+xoff, 707+yoff, 58, 30)
    pygame.draw.rect(screen, [0,0,0], exit_hitbox) 

    menu_hitbox = pygame.Rect(343.5+xoff, 10+yoff, 58, 30)
    pygame.draw.rect(screen, [0,0,0], menu_hitbox) 
    
    sound_hitbox = pygame.Rect(709+xoff, 709+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], sound_hitbox) 
    
    darkmode_hitbox = pygame.Rect(709+xoff, 10+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], darkmode_hitbox)

    fullscreen_hitbox = pygame.Rect(10+xoff, 709+yoff, 28, 28)
    pygame.draw.rect(screen, [0,0,0], fullscreen_hitbox) 

    #left gamemode buttons 
    player1_hitbox = pygame.Rect(2+xoff, 455+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], player1_hitbox) 

    ai1_hitbox = pygame.Rect(62+xoff, 455+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], ai1_hitbox) 

    #right gamemode buttons 
    player2_hitbox = pygame.Rect(652+xoff, 455+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], player2_hitbox) 

    ai2_hitbox = pygame.Rect(712+xoff, 455+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], ai2_hitbox) 

    
    #left AI difficulty buttons 
    ai1_d1_hitbox = pygame.Rect(2+xoff, 495+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], ai1_d1_hitbox) 

    ai1_d2_hitbox = pygame.Rect(32+xoff, 495+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], ai1_d2_hitbox) 

    ai1_d3_hitbox = pygame.Rect(62+xoff, 495+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], ai1_d3_hitbox) 

    #right AI difficulty buttons 
    ai2_d1_hitbox = pygame.Rect(652+xoff, 495+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], ai2_d1_hitbox) 

    ai2_d2_hitbox = pygame.Rect(682+xoff, 495+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], ai2_d2_hitbox) 

    ai2_d3_hitbox = pygame.Rect(712+xoff, 495+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], ai2_d3_hitbox) 


    #sprite hitboxes
    #left
    sprite_selection_hitbox1l = pygame.Rect(150+xoff, 150+yoff, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox1l) 
    
    sprite_selection_hitbox2l = pygame.Rect(150+xoff, 250+yoff, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox2l) 
    
    sprite_selection_hitbox3l = pygame.Rect(150+xoff, 350+yoff, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox3l) 
    
    sprite_selection_hitbox4l = pygame.Rect(150+xoff, 450+yoff, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox4l) 
    
    sprite_selection_hitbox5l = pygame.Rect(150+xoff, 550+yoff, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox5l) 
    
    l_hitboxes = [sprite_selection_hitbox1l, sprite_selection_hitbox2l, sprite_selection_hitbox3l, sprite_selection_hitbox4l, sprite_selection_hitbox5l]
    
    #right
    sprite_selection_hitbox1r = pygame.Rect(510+xoff, 150+yoff, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox1r) 
    
    sprite_selection_hitbox2r = pygame.Rect(510+xoff, 250+yoff, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox2r) 
    
    sprite_selection_hitbox3r = pygame.Rect(510+xoff, 350+yoff, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox3r) 
    
    sprite_selection_hitbox4r = pygame.Rect(510+xoff, 450+yoff, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox4r) 
    
    sprite_selection_hitbox5r = pygame.Rect(510+xoff, 550+yoff, 75, 75) 
    pygame.draw.rect(screen, [0,0,0], sprite_selection_hitbox5r) 
    
    r_hitboxes = [sprite_selection_hitbox1r, sprite_selection_hitbox2r, sprite_selection_hitbox3r, sprite_selection_hitbox4r, sprite_selection_hitbox5r]
    
                    
    if darkmode: 
        background = 'images/sprite_menu_v2_nuit.png'
    else: 
        background = 'images/sprite_menu_v2.png'
    sprite_background = pygame.image.load(background)
    screen.blit(sprite_background,(0+xoff,0+yoff))
    
    #define t_anim
    t_anim = int(time.time()*10)
    
    #triggered by random event? 
    #bird test
    if t_anim%2 == 1:
        bird_fly = pygame.image.load(bird)
    else:
        bird_fly = pygame.image.load(bird[:-4]+'2.png')
    screen.blit(bird_fly,(-745+20*(t_anim%500)+xoff, 100+yoff))
    
    
    #kitty test:
    if t_anim%2 == 1:
        cat_run = pygame.image.load(taby_cat)
    else:
        cat_run = pygame.image.load(taby_cat[:-4]+'_run.png')
    screen.blit(cat_run,(745-10*(t_anim%200)+xoff, 650+yoff))
    
    
    
    #make the buttons appear 
    pos = pygame.mouse.get_pos()

    if exit_hitbox.collidepoint(pos):
        exit_img = pygame.image.load('images/exit_hover.png')
    else : 
        exit_img = pygame.image.load('images/exit.png')
    screen.blit(exit_img, (343.5+xoff, 707+yoff)) 

    if menu_hitbox.collidepoint(pos):
        menu_img = pygame.image.load('images/go_menu_v2_hover.png')
    else : 
        menu_img = pygame.image.load('images/go_menu_v2.png')
    screen.blit(menu_img, (343.5+xoff, 10+yoff)) 
    
    if sound_hitbox.collidepoint(pos):
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2_selected.png')
    else : 
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2.png')
    screen.blit(sound_button, (709+xoff, 709+yoff))
    
    if darkmode: 
        darkmode_image = 'images/light_mode_v2.png'
    else: 
        darkmode_image = 'images/dark_mode_v2.png'
    if darkmode_hitbox.collidepoint(pos):
        darkmode_image = darkmode_image[:-4]+'_selected.png'
    darkmode_button = pygame.image.load(darkmode_image)
    screen.blit(darkmode_button, (709+xoff, 10+yoff))
    
    fullscreen_img = 'images/fullscreen' +('_on.png' if fullscreen else '.png')
    if fullscreen_hitbox.collidepoint(pos):
        fullscreen_img = fullscreen_img[:-4]+'_selected.png'
    screen.blit(pygame.image.load(fullscreen_img), (10+xoff, 709+yoff))

    #gamemode buttons 
    p1_gamemode, p2_gamemode = gamemodes 

    #left gamemode buttons 
    if p1_gamemode == "player":
        player1_image = 'images/player_clicked.png'
    else:
        player1_image = 'images/player.png'
    if player1_hitbox.collidepoint(pos):
        player1_image = player1_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(player1_image), (2+xoff, 455+yoff))

    if p1_gamemode == "player":
        ai1_image = 'images/AI.png'
    else:
        ai1_image = 'images/AI_clicked.png'
    if ai1_hitbox.collidepoint(pos):
        ai1_image = ai1_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(ai1_image), (62+xoff, 455+yoff))

    #right gamemode buttons 
    if p2_gamemode == "player":
        player2_image = 'images/player_clicked.png'
    else:
        player2_image = 'images/player.png'
    if player2_hitbox.collidepoint(pos):
        player2_image = player2_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(player2_image), (652+xoff, 455+yoff))

    if p2_gamemode == "player":
        ai2_image = 'images/AI.png'
    else:
        ai2_image = 'images/AI_clicked.png'
    if ai2_hitbox.collidepoint(pos):
        ai2_image = ai2_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(ai2_image), (712+xoff, 455+yoff))

    #left difficulty buttons 
    if p1_gamemode == "ai": 
        if difficulty[0] == 1:
            one_image = 'images/one_clicked.png'
        else:
            one_image = 'images/one.png'
        if ai1_d1_hitbox.collidepoint(pos):
            one_image = one_image[:-4]+'_hover.png'

        screen.blit(pygame.image.load(one_image), (2+xoff, 495+yoff))

        if difficulty[0] == 2:
            two_image = 'images/two_clicked.png'
        else:
            two_image = 'images/two.png'
        if ai1_d2_hitbox.collidepoint(pos):
            two_image = two_image[:-4]+'_hover.png'

        screen.blit(pygame.image.load(two_image), (32+xoff, 495+yoff))

        if difficulty[0] == 3:
            three_image = 'images/three_clicked.png'
        else:
            three_image = 'images/three.png'
        if ai1_d3_hitbox.collidepoint(pos):
            three_image = three_image[:-4]+'_hover.png'

        screen.blit(pygame.image.load(three_image), (62+xoff, 495+yoff))
        
    #right difficulty buttons 
    if p2_gamemode == "ai": 
        if difficulty[1] == 1:
            one_image = 'images/one_clicked.png'
        else:
            one_image = 'images/one.png'
        if ai2_d1_hitbox.collidepoint(pos):
            one_image = one_image[:-4]+'_hover.png'

        screen.blit(pygame.image.load(one_image), (652+xoff, 495+yoff))

        if difficulty[1] == 2:
            two_image = 'images/two_clicked.png'
        else:
            two_image = 'images/two.png'
        if ai2_d2_hitbox.collidepoint(pos):
            two_image = two_image[:-4]+'_hover.png'

        screen.blit(pygame.image.load(two_image), (682+xoff, 495+yoff))

        if difficulty[1] == 3:
            three_image = 'images/three_clicked.png'
        else:
            three_image = 'images/three.png'
        if ai2_d3_hitbox.collidepoint(pos):
            three_image = three_image[:-4]+'_hover.png'

        screen.blit(pygame.image.load(three_image), (712+xoff, 495+yoff))


    #show the current selected sprites 
    left_selected = pygame.image.load(img_p1)
    right_selected = pygame.image.load(img_p2)
    screen.blit(left_selected, (10+xoff, 375+yoff)) 
    screen.blit(right_selected, (660+xoff, 375+yoff)) 
    
    #show the other sprite options 
    sprite_options = [cherry, heart, red_circle, blue_cross, taby_cat] #all options
    for i in range(len(sprite_options)):
        if ((img_p1 == sprite_options[i]) or (img_p2 == sprite_options[i])): #if the sprite is already selected
            screen.blit(pygame.image.load("images/lock.png"), (150+xoff, 150+i*100+yoff))
            screen.blit(pygame.image.load("images/lock.png"), (510+xoff, 150+i*100+yoff))
        else:
            if l_hitboxes[i].collidepoint(pos): #if hovered
                if t_anim%10<5:
                    screen.blit(pygame.image.load(sprite_options[i][:-4]+'_run.png'), (150+xoff, 150+i*100+yoff)) #left
                else:
                    screen.blit(pygame.image.load(sprite_options[i]), (150+xoff, 150+i*100+yoff)) #left
                screen.blit(pygame.image.load(sprite_options[i]), (510+xoff, 150+i*100+yoff)) #right  
            elif r_hitboxes[i].collidepoint(pos):
                if t_anim%10<5:
                    screen.blit(pygame.image.load(sprite_options[i][:-4]+'_run.png'), (510+xoff, 150+i*100+yoff)) #right
                else:
                    screen.blit(pygame.image.load(sprite_options[i]), (510+xoff, 150+i*100+yoff)) #right
                screen.blit(pygame.image.load(sprite_options[i]), (150+xoff, 150+i*100+yoff)) #left
            
            else:
                screen.blit(pygame.image.load(sprite_options[i]), (510+xoff, 150+i*100+yoff)) #right
                screen.blit(pygame.image.load(sprite_options[i]), (150+xoff, 150+i*100+yoff)) #left
    
    
    #sounds 
    lock = pygame.mixer.Sound("sounds/lock.wav")
    if cat_is_dog: 
        meow = pygame.mixer.Sound("sounds/mario-bark.mp3")
    else: 
        meow = pygame.mixer.Sound("sounds/mario-meow.mp3")
    munch = pygame.mixer.Sound("sounds/munch_1.wav")
    select = pygame.mixer.Sound("sounds/arcade-bonus.wav")
    
    #make the background appear 
    if fullscreen: 
        if darkmode:
            background_img = "images/background_nuit.png"
        else:
            background_img = "images/background.png"
        infoObject = pygame.display.Info()
        screen.blit(pygame.image.load(background_img), ((infoObject.current_w - 1920)/2, (infoObject.current_h - 1080)/2))

    #handle events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            game = True
        elif event.type == pygame.K_q:
            done = True
            game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #buttons clicked -> consequences
            if exit_hitbox.collidepoint(pos):
                done = True    
                game = True 

            #left gamemode buttons
            if player1_hitbox.collidepoint(pos):
                p1_gamemode = "player"

            if ai1_hitbox.collidepoint(pos):
                p1_gamemode = "ai"
            
            #right gamemode buttons 
            if player2_hitbox.collidepoint(pos):
                p2_gamemode = "player"

            if ai2_hitbox.collidepoint(pos):
                p2_gamemode = "ai"

            #left AI difficulty buttons 
            if ai1_d1_hitbox.collidepoint(pos):
                _, d2 = difficulty
                difficulty = (1, d2) 

            if ai1_d2_hitbox.collidepoint(pos):
                _, d2 = difficulty
                difficulty = (2, d2) 

            if ai1_d3_hitbox.collidepoint(pos):
                _, d2 = difficulty
                difficulty = (3, d2) 

            #right AI difficulty buttons 
            if ai2_d1_hitbox.collidepoint(pos):
                d1, _ = difficulty
                difficulty = (d1, 1) 

            if ai2_d2_hitbox.collidepoint(pos):
                d1, _ = difficulty
                difficulty = (d1, 2) 

            if ai2_d3_hitbox.collidepoint(pos):
                d1, _ = difficulty
                difficulty = (d1, 3) 


            #left
            if sprite_selection_hitbox1l.collidepoint(pos):
                if ((img_p1 != cherry) and (img_p2 != cherry)): #if click on a sprite for a player and it isn't already selected
                    img_p1 = cherry
                    if sound_on: 
                        pygame.mixer.Sound.play(munch)
                elif sound_on:
                    pygame.mixer.Sound.play(lock)
                    
            if sprite_selection_hitbox2l.collidepoint(pos):
                if ((img_p1 != heart) and (img_p2 != heart)): 
                    img_p1 = heart
                    if sound_on: 
                        pygame.mixer.Sound.play(select)
                elif sound_on:
                    pygame.mixer.Sound.play(lock)

            if sprite_selection_hitbox3l.collidepoint(pos):
                if ((img_p1 != red_circle) and (img_p2 != red_circle)): 
                    img_p1 = red_circle
                    if sound_on: 
                        pygame.mixer.Sound.play(select)
                elif sound_on:
                    pygame.mixer.Sound.play(lock)
                
            if sprite_selection_hitbox4l.collidepoint(pos):
                if ((img_p1 != blue_cross) and (img_p2 != blue_cross)): 
                    img_p1 = blue_cross
                    if sound_on: 
                        pygame.mixer.Sound.play(select)
                elif sound_on:
                    pygame.mixer.Sound.play(lock)
            
            if sprite_selection_hitbox5l.collidepoint(pos):
                if ((img_p1 != taby_cat) and (img_p2 != taby_cat)): 
                    img_p1 = taby_cat
                    if sound_on: 
                        pygame.mixer.Sound.play(meow)
                elif sound_on:
                    pygame.mixer.Sound.play(lock)
            
            #right
            if sprite_selection_hitbox1r.collidepoint(pos):
                if ((img_p1 != cherry) and (img_p2 != cherry)): #if click on a sprite for a player and it isn't already selected
                    img_p2 = cherry
                    if sound_on: 
                        pygame.mixer.Sound.play(munch)
                elif sound_on:
                    pygame.mixer.Sound.play(lock)
            
            if sprite_selection_hitbox2r.collidepoint(pos):
                if ((img_p1 != heart) and (img_p2 != heart)): 
                    img_p2 = heart
                    if sound_on: 
                        pygame.mixer.Sound.play(select)
                elif sound_on:
                    pygame.mixer.Sound.play(lock)
                
            if sprite_selection_hitbox3r.collidepoint(pos):
                if ((img_p1 != red_circle) and (img_p2 != red_circle)): 
                    img_p2 = red_circle
                    if sound_on: 
                        pygame.mixer.Sound.play(select)
                elif sound_on:
                    pygame.mixer.Sound.play(lock)
                
            if sprite_selection_hitbox4r.collidepoint(pos):
                if ((img_p1 != blue_cross) and (img_p2 != blue_cross)): 
                    img_p2 = blue_cross
                    if sound_on: 
                        pygame.mixer.Sound.play(select)
                elif sound_on:
                    pygame.mixer.Sound.play(lock)
            
            if sprite_selection_hitbox5r.collidepoint(pos):
                if ((img_p1 != taby_cat) and (img_p2 != taby_cat)): 
                    img_p2 = taby_cat
                    if sound_on: 
                        pygame.mixer.Sound.play(meow)
                elif sound_on:
                    pygame.mixer.Sound.play(lock)
            
            if sound_hitbox.collidepoint(pos):
                if sound_on : 
                    pygame.mixer.music.stop()
                    sound_on = False 
                else : 
                    sound_on = True
                    pygame.mixer.music.load(sprite_theme)
                    pygame.mixer.music.play(-1)
            
            if menu_hitbox.collidepoint(pos):
                kitty_transition(offset, fullscreen, darkmode)
                if sound_on:
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)
                in_menu = True
            
            if darkmode_hitbox.collidepoint(pos): 
                if darkmode: 
                    darkmode = False
                else: 
                    darkmode = True
    
            if fullscreen_hitbox.collidepoint(pos): 
                if fullscreen: 
                    screen = pygame.display.set_mode(WINDOW_SIZE)
                    offset = (0,0)
                else: 
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    infoObject = pygame.display.Info()
                    offset = ((infoObject.current_w-745)/2, (infoObject.current_h-745)/2)
                fullscreen = not fullscreen #becomes False if True, True if False 

    clock.tick(60)
        
    pygame.display.flip()

    return (done, game, in_menu, screen, fullscreen, offset, (p1_gamemode, p2_gamemode), difficulty)


def kitty_transition(offset, fullscreen, darkmode):
    '''Transition used to go from a menu to another. 
    Includes a cat running across the screen with a rainbow behind it.'''
    go = "sounds/cattrill.mp3"
    global done 
    global game
    
    xoff, yoff = offset 

    if sound_on:
        pygame.mixer.music.load(go)
        pygame.mixer.music.play()

    t = 0
    while t<90:
        if (t//10)%2 == 0:
            t_run = pygame.image.load(transition0)
        else:
            t_run = pygame.image.load(transition1)
        screen.blit(t_run,((740+2*xoff)-220*(t//10), 0+yoff))
        
        if not fullscreen:
            t += 1
        else: 
            t += 3 #to speed the animation up in fullscreen 

            #background in case we're in fullscreen 
            if darkmode:
                background_img = "images/background_nuit.png"
            else:
                background_img = "images/background.png"
            infoObject = pygame.display.Info()
            screen.blit(pygame.image.load(background_img), ((infoObject.current_w - 1920)/2, (infoObject.current_h - 1080)/2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                game = True
            elif event.type == pygame.K_q:
                done = True
                game = True
        clock.tick(60)
    
        pygame.display.flip()


def online_select(done, game, in_menu, screen, connect, fullscreen, offset, gamemodes):
    """Menu for the online selection (HOST or GUEST)"""
    global sound_on
    global img_p1
    global img_p2
    global darkmode

    xoff, yoff = offset

    #make the button hitboxes
    menu_hitbox = pygame.Rect(343.5+xoff, 10+yoff, 58, 30)
    pygame.draw.rect(screen, [0,0,0], menu_hitbox)

    sound_hitbox = pygame.Rect(709+xoff, 709+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], sound_hitbox)

    darkmode_hitbox = pygame.Rect(709+xoff, 10+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], darkmode_hitbox)

    fullscreen_hitbox = pygame.Rect(10+xoff, 709+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], fullscreen_hitbox)

    host_hitbox = pygame.Rect(258.5+xoff, 375+yoff, 78, 30)
    pygame.draw.rect(screen, [0,0,0], host_hitbox)

    guest_hitbox = pygame.Rect(412.5+xoff, 375+yoff, 78, 30)
    pygame.draw.rect(screen, [0,0,0], guest_hitbox)

    if darkmode:
        background = 'images/sprite_menu_v2_nuit.png'
    else:
        background = 'images/sprite_menu_v2.png'
    sprite_background = pygame.image.load(background)
    screen.blit(sprite_background,(0+xoff,0+yoff))

    #define t_anim
    t_anim = int(time.time()*10)

    #triggered by random event?
    #bird test
    if t_anim%2 == 1:
        bird_fly = pygame.image.load(bird)
    else:
        bird_fly = pygame.image.load(bird[:-4]+'2.png')
    screen.blit(bird_fly,(-745+20*(t_anim%500)+xoff, 100+yoff))


    #kitty test:
    if t_anim%2 == 1:
        cat_run = pygame.image.load(taby_cat)
    else:
        cat_run = pygame.image.load(taby_cat[:-4]+'_run.png')
    screen.blit(cat_run,(745-10*(t_anim%200)+xoff, 650+yoff))


    #make the buttons appear
    pos = pygame.mouse.get_pos()
    if menu_hitbox.collidepoint(pos):
        menu_img = pygame.image.load('images/go_menu_v2_hover.png')
    else :
        menu_img = pygame.image.load('images/go_menu_v2.png')
    screen.blit(menu_img, (343.5+xoff, 10+yoff))

    if sound_hitbox.collidepoint(pos):
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2_selected.png')
    else :
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2.png')
    screen.blit(sound_button, (709+xoff, 709+yoff))

    if darkmode:
        darkmode_image = 'images/light_mode_v2.png'
    else:
        darkmode_image = 'images/dark_mode_v2.png'
    if darkmode_hitbox.collidepoint(pos):
        darkmode_image = darkmode_image[:-4]+'_selected.png'
    darkmode_button = pygame.image.load(darkmode_image)
    screen.blit(darkmode_button, (709+xoff, 10+yoff))

    if fullscreen_hitbox.collidepoint(pos):
        fullscreen_img = pygame.image.load('images/fullscreen_selected.png')
    else :
        fullscreen_img = pygame.image.load('images/fullscreen.png')
    screen.blit(fullscreen_img, (10+xoff, 709+yoff))

    if host_hitbox.collidepoint(pos):
        host_img = pygame.image.load('images/host_hover.png')
    else :
        host_img = pygame.image.load('images/host.png')
    screen.blit(host_img, (258.5+xoff, 375+yoff))

    if guest_hitbox.collidepoint(pos):
        guest_img = pygame.image.load('images/guest_hover.png')
    else :
        guest_img = pygame.image.load('images/guest.png')
    screen.blit(guest_img, (412.5+xoff, 375+yoff))

    #gamemode buttons
    p1_gamemode, p2_gamemode = gamemodes

    #sounds
    lock = pygame.mixer.Sound("sounds/lock.wav")

    #make the background appear
    if fullscreen:
        if darkmode:
            background_img = "images/background_nuit.png"
        else:
            background_img = "images/background.png"
        infoObject = pygame.display.Info()
        screen.blit(pygame.image.load(background_img), ((infoObject.current_w - 1920)/2, (infoObject.current_h - 1080)/2))

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            game = True
        elif event.type == pygame.K_q:
            done = True
            game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #buttons clicked -> consequences

            if menu_hitbox.collidepoint(pos):
                kitty_transition(offset, fullscreen, darkmode)
                if sound_on:
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)
                in_menu = True

            if sound_hitbox.collidepoint(pos):
                if sound_on :
                    pygame.mixer.music.stop()
                    sound_on = False
                else :
                    sound_on = True
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)

            #host buttons
            if host_hitbox.collidepoint(pos):
                p1_gamemode = "other"
                kitty_transition(offset, fullscreen, darkmode)
                if sound_on:
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)
                connect = True

            #guest buttons
            if guest_hitbox.collidepoint(pos):
                p2_gamemode = "other"
                kitty_transition(offset, fullscreen, darkmode)
                if sound_on:
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)
                connect = True

            if darkmode_hitbox.collidepoint(pos):
                if darkmode:
                    darkmode = False
                else:
                    darkmode = True

            if fullscreen_hitbox.collidepoint(pos):
                if fullscreen:
                    screen = pygame.display.set_mode(WINDOW_SIZE)
                    offset = (0,0)
                else:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    infoObject = pygame.display.Info()
                    offset = ((infoObject.current_w-745)/2, (infoObject.current_h-745)/2)
                fullscreen = not fullscreen #becomes False if True, True if False

    clock.tick(60)

    pygame.display.flip()

    return (done, game, in_menu, screen, connect, fullscreen, offset, (p1_gamemode, p2_gamemode))


def host_connect(done, game, in_menu, screen, ip, port, pseudo, valid, connection, connect, fullscreen, offset, gamemodes):
    """Menu for the connection when we are host"""
    global sound_on
    global img_p1
    global img_p2
    global darkmode
    global active
    global color_pseudo

    xoff, yoff = offset

    #make the button hitboxes
    menu_hitbox = pygame.Rect(343.5+xoff, 10+yoff, 58, 30)
    pygame.draw.rect(screen, [0,0,0], menu_hitbox)

    sound_hitbox = pygame.Rect(709+xoff, 709+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], sound_hitbox)

    darkmode_hitbox = pygame.Rect(709+xoff, 10+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], darkmode_hitbox)

    fullscreen_hitbox = pygame.Rect(10+xoff, 709+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], fullscreen_hitbox)

    connection_hitbox = pygame.Rect(343.5+xoff, 500+yoff, 58, 30)
    pygame.draw.rect(screen, [0,0,0], connection_hitbox)

    if darkmode:
        background = 'images/sprite_menu_v2_nuit.png'
    else:
        background = 'images/sprite_menu_v2.png'
    sprite_background = pygame.image.load(background)
    screen.blit(sprite_background,(0+xoff,0+yoff))

    #define t_anim
    t_anim = int(time.time()*10)

    #triggered by random event?
    #bird test
    if t_anim%2 == 1:
        bird_fly = pygame.image.load(bird)
    else:
        bird_fly = pygame.image.load(bird[:-4]+'2.png')
    screen.blit(bird_fly,(-745+20*(t_anim%500)+xoff, 100+yoff))


    #kitty test:
    if t_anim%2 == 1:
        cat_run = pygame.image.load(taby_cat)
    else:
        cat_run = pygame.image.load(taby_cat[:-4]+'_run.png')
    screen.blit(cat_run,(745-10*(t_anim%200)+xoff, 650+yoff))


    #make the buttons appear
    pos = pygame.mouse.get_pos()
    if menu_hitbox.collidepoint(pos):
        menu_img = pygame.image.load('images/go_menu_v2_hover.png')
    else :
        menu_img = pygame.image.load('images/go_menu_v2.png')
    screen.blit(menu_img, (343.5+xoff, 10+yoff))

    if sound_hitbox.collidepoint(pos):
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2_selected.png')
    else :
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2.png')
    screen.blit(sound_button, (709+xoff, 709+yoff))

    if darkmode:
        darkmode_image = 'images/light_mode_v2.png'
    else:
        darkmode_image = 'images/dark_mode_v2.png'
    if darkmode_hitbox.collidepoint(pos):
        darkmode_image = darkmode_image[:-4]+'_selected.png'
    darkmode_button = pygame.image.load(darkmode_image)
    screen.blit(darkmode_button, (709+xoff, 10+yoff))

    if fullscreen_hitbox.collidepoint(pos):
        fullscreen_img = pygame.image.load('images/fullscreen_selected.png')
    else :
        fullscreen_img = pygame.image.load('images/fullscreen.png')
    screen.blit(fullscreen_img, (10+xoff, 709+yoff))

    if connection_hitbox.collidepoint(pos):
        connection_img = pygame.image.load('images/start_v2_hover.png')
    else :
        connection_img = pygame.image.load('images/start_v2.png')
    if valid:
        screen.blit(connection_img, (343.5+xoff, 500+yoff))

    #sounds
    lock = pygame.mixer.Sound("sounds/lock.wav")

    #make the background appear
    if fullscreen:
        if darkmode:
            background_img = "images/background_nuit.png"
        else:
            background_img = "images/background.png"
        infoObject = pygame.display.Info()
        screen.blit(pygame.image.load(background_img), ((infoObject.current_w - 1920)/2, (infoObject.current_h - 1080)/2))

    #add text
    font = pygame.font.Font('Minecraft.ttf', 32)

    ip_text_surface = font.render(f"This is your IP Address: {ip}", True, (255,255,255))
    port_text_surface = font.render(f"This is the port for the connection: {port}", True, (255,255,255))

    ip_text_rect = ip_text_surface.get_rect(center=(totxsize//2+xoff, totysize//2 - 150 +yoff))
    port_text_rect = port_text_surface.get_rect(center=(totxsize//2+xoff, totysize//2 - 100+yoff))

    screen.blit(ip_text_surface, ip_text_rect)
    screen.blit(port_text_surface, port_text_rect)

    #add text input bloc for pseudo
    input_box = pygame.Rect(totxsize//2 - 100+xoff, totysize//2 - 25+yoff, 200, 50)
    txt_surface = font.render(pseudo, True, color_pseudo)
    txt_surface_rect = txt_surface.get_rect(center=(totxsize//2+xoff, totysize//2+yoff))
    screen.blit(txt_surface, txt_surface_rect)
    pygame.draw.rect(screen, color_pseudo, input_box, 2)

    #gamemode buttons
    p1_gamemode, p2_gamemode = gamemodes

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            game = True
        elif event.type == pygame.K_q:
            done = True
            game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #buttons clicked -> consequences

            if menu_hitbox.collidepoint(pos):
                kitty_transition(offset, fullscreen, darkmode)
                if sound_on:
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)
                in_menu = True
                connect = False
                p1_gamemode = "player"

            if sound_hitbox.collidepoint(pos):
                if sound_on :
                    pygame.mixer.music.stop()
                    sound_on = False
                else :
                    sound_on = True
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)

            if darkmode_hitbox.collidepoint(pos):
                if darkmode:
                    darkmode = False
                else:
                    darkmode = True

            if fullscreen_hitbox.collidepoint(pos):
                if fullscreen:
                    screen = pygame.display.set_mode(WINDOW_SIZE)
                    offset = (0,0)
                else:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    infoObject = pygame.display.Info()
                    offset = ((infoObject.current_w-745)/2, (infoObject.current_h-745)/2)
                fullscreen = not fullscreen #becomes False if True, True if False

            if connection_hitbox.collidepoint(pos):
                if valid:
                    connection = True

            # If the user clicked on the input_box rect.
            if input_box.collidepoint(pos):
                # Toggle the active variable.
                active = (active + 1) % 2
            # Change the current color of the input box.
            color_pseudo= color_active if active == 1 else color_inactive

        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    pseudo = pseudo[:-1]
                else:
                    pseudo += event.unicode

    clock.tick(60)

    pygame.display.flip()

    return (done, game, in_menu, screen, pseudo, connection, connect, fullscreen, offset, (p1_gamemode, p2_gamemode))


def guest_connect(done, game, in_menu, screen, ip, port, pseudo, valid, connection, connect, fullscreen, offset, gamemodes):
    """Menu for the connection when we are guest"""
    global sound_on
    global img_p1
    global img_p2
    global darkmode
    global active
    global color_pseudo
    global color_ip
    global color_port

    xoff, yoff = offset

    #make the button hitboxes
    menu_hitbox = pygame.Rect(343.5+xoff, 10+yoff, 58, 30)
    pygame.draw.rect(screen, [0,0,0], menu_hitbox)

    sound_hitbox = pygame.Rect(709+xoff, 709+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], sound_hitbox)

    darkmode_hitbox = pygame.Rect(709+xoff, 10+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], darkmode_hitbox)

    fullscreen_hitbox = pygame.Rect(10+xoff, 709+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], fullscreen_hitbox)

    connection_hitbox = pygame.Rect(343.5+xoff, 500+yoff, 58, 30)
    pygame.draw.rect(screen, [0,0,0], connection_hitbox)

    if darkmode:
        background = 'images/sprite_menu_v2_nuit.png'
    else:
        background = 'images/sprite_menu_v2.png'
    sprite_background = pygame.image.load(background)
    screen.blit(sprite_background,(0+xoff,0+yoff))

    #define t_anim
    t_anim = int(time.time()*10)

    #triggered by random event?
    #bird test
    if t_anim%2 == 1:
        bird_fly = pygame.image.load(bird)
    else:
        bird_fly = pygame.image.load(bird[:-4]+'2.png')
    screen.blit(bird_fly,(-745+20*(t_anim%500)+xoff, 100+yoff))


    #kitty test:
    if t_anim%2 == 1:
        cat_run = pygame.image.load(taby_cat)
    else:
        cat_run = pygame.image.load(taby_cat[:-4]+'_run.png')
    screen.blit(cat_run,(745-10*(t_anim%200)+xoff, 650+yoff))


    #make the buttons appear
    pos = pygame.mouse.get_pos()
    if menu_hitbox.collidepoint(pos):
        menu_img = pygame.image.load('images/go_menu_v2_hover.png')
    else :
        menu_img = pygame.image.load('images/go_menu_v2.png')
    screen.blit(menu_img, (343.5+xoff, 10+yoff))

    if sound_hitbox.collidepoint(pos):
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2_selected.png')
    else :
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2.png')
    screen.blit(sound_button, (709+xoff, 709+yoff))

    if darkmode:
        darkmode_image = 'images/light_mode_v2.png'
    else:
        darkmode_image = 'images/dark_mode_v2.png'
    if darkmode_hitbox.collidepoint(pos):
        darkmode_image = darkmode_image[:-4]+'_selected.png'
    darkmode_button = pygame.image.load(darkmode_image)
    screen.blit(darkmode_button, (709+xoff, 10+yoff))

    if fullscreen_hitbox.collidepoint(pos):
        fullscreen_img = pygame.image.load('images/fullscreen_selected.png')
    else :
        fullscreen_img = pygame.image.load('images/fullscreen.png')
    screen.blit(fullscreen_img, (10+xoff, 709+yoff))

    if connection_hitbox.collidepoint(pos):
        connection_img = pygame.image.load('images/start_v2_hover.png')
    else :
        connection_img = pygame.image.load('images/start_v2.png')
    if valid:
        screen.blit(connection_img, (343.5+xoff, 500+yoff))

    #sounds
    lock = pygame.mixer.Sound("sounds/lock.wav")

    #make the background appear
    if fullscreen:
        if darkmode:
            background_img = "images/background_nuit.png"
        else:
            background_img = "images/background.png"
        infoObject = pygame.display.Info()
        screen.blit(pygame.image.load(background_img), ((infoObject.current_w - 1920)/2, (infoObject.current_h - 1080)/2))

    #add text

    font = pygame.font.Font('Minecraft.ttf', 32)

    pseudo_text_surface = font.render("Pseudo:", True, (255,255,255))
    ip_text_surface = font.render("IP Address:", True, (255,255,255))
    port_text_surface = font.render("Port:", True, (255,255,255))

    pseudo_text_rect = ip_text_surface.get_rect(center=(totxsize//2 - 220 + xoff, totysize//2 - 75 + yoff))
    ip_text_rect = ip_text_surface.get_rect(center=(totxsize//2 + xoff, totysize//2 - 75 + yoff))
    port_text_rect = port_text_surface.get_rect(center=(totxsize//2 + 220 + xoff, totysize//2 - 75 + yoff))

    screen.blit(pseudo_text_surface, pseudo_text_rect)
    screen.blit(ip_text_surface, ip_text_rect)
    screen.blit(port_text_surface, port_text_rect)

    #add text input bloc for pseudo
    pseudo_input_box = pygame.Rect(totxsize//2 - 320+xoff, totysize//2 - 25+yoff, 200, 50)
    txt_surface = font.render(pseudo, True, color_pseudo)
    txt_surface_rect = txt_surface.get_rect(center=(totxsize//2+xoff - 220, totysize//2+yoff))
    screen.blit(txt_surface, txt_surface_rect)
    pygame.draw.rect(screen, color_pseudo, pseudo_input_box, 2)

    ip_input_box = pygame.Rect(totxsize//2 - 100+xoff, totysize//2 - 25+yoff, 200, 50)
    txt_surface = font.render(ip, True, color_ip)
    txt_surface_rect = txt_surface.get_rect(center=(totxsize//2+xoff, totysize//2+yoff))
    screen.blit(txt_surface, txt_surface_rect)
    pygame.draw.rect(screen, color_ip, ip_input_box, 2)

    port_input_box = pygame.Rect(totxsize//2 + 120+xoff, totysize//2 - 25+yoff, 200, 50)
    txt_surface = font.render(port, True, color_port)
    txt_surface_rect = txt_surface.get_rect(center=(totxsize//2+xoff + 220, totysize//2+yoff))
    screen.blit(txt_surface, txt_surface_rect)
    pygame.draw.rect(screen, color_port, port_input_box, 2)

    #gamemode buttons
    p1_gamemode, p2_gamemode = gamemodes

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            game = True
        elif event.type == pygame.K_q:
            done = True
            game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #buttons clicked -> consequences

            if menu_hitbox.collidepoint(pos):
                kitty_transition(offset, fullscreen, darkmode)
                if sound_on:
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)
                in_menu = True
                connect = False
                p2_gamemode = "player"

            if sound_hitbox.collidepoint(pos):
                if sound_on :
                    pygame.mixer.music.stop()
                    sound_on = False
                else :
                    sound_on = True
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)

            if darkmode_hitbox.collidepoint(pos):
                if darkmode:
                    darkmode = False
                else:
                    darkmode = True

            if fullscreen_hitbox.collidepoint(pos):
                if fullscreen:
                    screen = pygame.display.set_mode(WINDOW_SIZE)
                    offset = (0,0)
                else:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    infoObject = pygame.display.Info()
                    offset = ((infoObject.current_w-745)/2, (infoObject.current_h-745)/2)
                fullscreen = not fullscreen #becomes False if True, True if False

            if connection_hitbox.collidepoint(pos):
                if valid:
                    connection = True

            # If the user clicked on the input_box rect.
            if pseudo_input_box.collidepoint(pos):
                # Toggle the active variable.
                active = 0 if active == 1 else 1

            if ip_input_box.collidepoint(pos):
                active = 0 if active == 2 else 2

            if port_input_box.collidepoint(pos):
                active = 0 if active == 3 else 3

            # Change the current color of the input box.
            color_pseudo= color_active if active == 1 else color_inactive
            color_ip = color_active if active == 2 else color_inactive
            color_port = color_active if active == 3 else color_inactive

        elif event.type == pygame.KEYDOWN:
            if active == 1:
                if event.key == pygame.K_BACKSPACE:
                    pseudo = pseudo[:-1]
                else:
                    pseudo += event.unicode
            if active == 2:
                if event.key == pygame.K_BACKSPACE:
                    ip = ip[:-1]
                else:
                    ip += event.unicode
            if active == 3:
                if event.key == pygame.K_BACKSPACE:
                    port = port[:-1]
                else:
                    port += event.unicode

    clock.tick(60)

    pygame.display.flip()

    return (done, game, in_menu, screen, ip, port, pseudo, connection, connect, fullscreen, offset, (p1_gamemode, p2_gamemode))


def waiting_screen(offset):
    """Waiting screen"""
    global sound_on
    global darkmode

    xoff, yoff = offset

    if darkmode:
        background = 'images/sprite_menu_v2_nuit.png'
    else:
        background = 'images/sprite_menu_v2.png'
    sprite_background = pygame.image.load(background)
    screen.blit(sprite_background,(0+xoff,0+yoff))

    #add text
    font = pygame.font.Font('Minecraft.ttf', 32)

    waiting_text_surface = font.render("Waiting for connection...", True, (255,255,255))

    waiting_text_rect = waiting_text_surface.get_rect(center=(totxsize//2+xoff, totysize//2 - 150 +yoff))

    screen.blit(waiting_text_surface, waiting_text_rect)

    clock.tick(60)

    pygame.display.flip()


def error_screen(offset):
    """Error screen, end of game"""
    global sound_on
    global darkmode

    xoff, yoff = offset

    if darkmode:
        background = 'images/sprite_menu_v2_nuit.png'
    else:
        background = 'images/sprite_menu_v2.png'
    sprite_background = pygame.image.load(background)
    screen.blit(sprite_background,(0+xoff,0+yoff))

    #add text
    font = pygame.font.Font('Minecraft.ttf', 32)

    waiting_text_surface = font.render("An errors occurs...", True, (255,255,255))

    waiting_text_rect = waiting_text_surface.get_rect(center=(totxsize//2+xoff, totysize//2 - 150 +yoff))

    screen.blit(waiting_text_surface, waiting_text_rect)

    clock.tick(60)

    pygame.display.flip()


def game_menu(done, last_move, game_over, grid, TotalGrid, offset, fullscreen, allowedx, allowedy, in_settings, redPlaying, online, pseudo, pseudo_adv, gamemodes): 
    """Draws the play grid."""
    global playcolour

    xoff, yoff = offset 
    p1_gamemode, p2_gamemode = gamemodes

    if darkmode:
        BLACK = (255, 255, 255)
        WHITE = (0, 0, 0)
    else:
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)

    if redPlaying: 
        playcolour = (((200,0,0) if darkmode else (0,255,0)))
    else:
        playcolour = ((0, 200, 200) if darkmode else (255,0,0))

    # settings button hitbox
    settings_hitbox = pygame.Rect(10+xoff, yoff, 40, 10)
    pygame.draw.rect(screen, [0,0,0], settings_hitbox) 

    #grid background 
    screen.fill(BLACK)

    #placeholder background 
    if darkmode: 
        background = 'images/sprite_menu_v2_nuit.png'
    else: 
        background = 'images/sprite_menu_v2.png'
    sprite_background = pygame.image.load(background)
    screen.blit(sprite_background,(745+xoff,0+yoff))

    #when placeholder background: 
    #add text
    font = pygame.font.Font('Minecraft.ttf', 20)

    font_color = (255,255,255) if darkmode else (0,0,0)

    line_1 = font.render(f"Next player:", True, font_color)

    line_1_rect = line_1.get_rect(center=(745 + totxsize//2+xoff, totysize//2+yoff-50))

    screen.blit(line_1, line_1_rect)

    if redPlaying: 
        next = img_p1
    else: 
        next = img_p2
    next_player = pygame.image.load(next)
    screen.blit(next_player,(1080+xoff,335+yoff))

    # Show pseudos when online 
    if online: 
        if (redPlaying and p1_gamemode == 'other') or (not redPlaying and p2_gamemode == 'other'):
            line_2 = font.render(f"{pseudo_adv}, it's your turn!", True, font_color)
        elif (not redPlaying and p1_gamemode == 'other') or (redPlaying and p2_gamemode == 'other'):
            line_2 = font.render(f"{pseudo}, it's your turn!", True, font_color)
        
        line_2_rect = line_2.get_rect(center=(745 + totxsize//2+xoff, totysize//2+yoff+50))

        screen.blit(line_2, line_2_rect)

    #play square 
    #if allowedx == -1 and allowedy == -1:
    #    allowed_square = pygame.Rect(xoff+5, yoff+5, 735, 735)
    #else:
    #    allowed_square = pygame.Rect(allowedx*(MARGIN+WIDTH) + 2*MARGIN + xoff + ((allowedx//3 -1) *MARGIN) , allowedx*(MARGIN+WIDTH) + 2*MARGIN + xoff + ((allowedx//3 -1) *MARGIN) , 245, 245)
    #pygame.draw.rect(screen, [128,128,128], allowed_square) 
    
    # Draw the grid
    extramarginx = 0
    extramarginy = 0

    for row in range(amtrow):
        if row%3 == 0:
            extramarginy = extramarginy + MARGIN 
        for column in range(amtcol):
            w = False #to see if an image needs to be drawn
            if column%3 == 0:
                extramarginx = extramarginx + MARGIN
            ResizePlayBox(playrect, allowedx, allowedy, HEIGHT, WIDTH, offset)
            pygame.draw.rect(screen, WHITE,[((MARGIN + WIDTH) * column) + MARGIN + extramarginx+xoff,((MARGIN + HEIGHT) * row) + MARGIN + extramarginy+yoff,WIDTH,HEIGHT])
            pygame.draw.rect(screen, playcolour, playrect, playwidth)
            if grid[column][row] == 1:
                w = True
                img = pygame.image.load(img_p1)
            if grid[column][row] == 2:
                w = True
                img = pygame.image.load(img_p2)
            if w : 
                screen.blit(img, (((MARGIN + WIDTH) * column) + MARGIN + extramarginx+xoff,
                              ((MARGIN + HEIGHT) * row) + MARGIN+ extramarginy+yoff))
                
        extramarginx = 0

    # settings button 
    pos = pygame.mouse.get_pos()
    settings_img = 'images/settings' +('_hover.png' if settings_hitbox.collidepoint(pos) else '.png')
    screen.blit(pygame.image.load(settings_img), (10+xoff, yoff))

    # Set the screen background
    if fullscreen: 
        if darkmode:
            background_img = "images/background_v2_nuit.png"
        else:
            background_img = "images/background_v2.png"
        infoObject = pygame.display.Info()
        screen.blit(pygame.image.load(background_img), ((infoObject.current_w - 2194)/2, (infoObject.current_h - 1080)/2))

    clock.tick(60)
        
    pygame.display.flip()

    return (done, last_move, game_over, grid, TotalGrid, HEIGHT, WIDTH, offset, in_settings)


def settings_menu(done, game, in_menu, screen, fullscreen, offset, in_settings, nb_fingers, select_mouse):
    """Menu to change settings in game"""
    global sound_on 
    global darkmode
    
    xoff, yoff = offset 

    #make the button hitboxes
    exit_hitbox = pygame.Rect(343.5+xoff, 707+yoff, 58, 30)
    pygame.draw.rect(screen, [0,0,0], exit_hitbox) 

    sound_hitbox = pygame.Rect(709+xoff, 709+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], sound_hitbox) 
    
    darkmode_hitbox = pygame.Rect(709+xoff, 10+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], darkmode_hitbox)

    settings_hitbox = pygame.Rect(10+xoff, yoff, 40, 10)
    pygame.draw.rect(screen, [0,0,0], settings_hitbox) 

    #object tracking button hitboxes 
    zero_hitbox = pygame.Rect(105+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], zero_hitbox) 

    one_hitbox = pygame.Rect(205+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], one_hitbox) 

    two_hitbox = pygame.Rect(305+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], two_hitbox) 

    three_hitbox = pygame.Rect(405+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], three_hitbox) 

    four_hitbox = pygame.Rect(505+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], four_hitbox) 

    mouse_hitbox = pygame.Rect(605+xoff, 400+yoff, 30, 30)
    pygame.draw.rect(screen, [0,0,0], mouse_hitbox) 


    if darkmode: 
        background = 'images/sprite_menu_v2_nuit.png'
    else: 
        background = 'images/sprite_menu_v2.png'
    sprite_background = pygame.image.load(background)
    screen.blit(sprite_background,(0+xoff,0+yoff))
    screen.blit(sprite_background,(745+xoff,0+yoff))

    #add text
    font = pygame.font.Font('Minecraft.ttf', 13)

    font_color = (255,255,255) if darkmode else (0,0,0)

    line_1 = font.render(f"Welcome to Super Retro Tic Tac Toe!", True, font_color)
    line_2 = font.render(f"This game is played on a tic-tac-toe board made up of 9 small boards.", True, font_color)
    line_3 = font.render(f"Win 3 small boards in a row (vertical, horizontal or diagonal) to win the game!", True, font_color)
    line_4 = font.render(f"You can only play in the small board placed where the opponent played in their own small board the previous turn.", True, font_color)
    line_5 = font.render(f"To activate hand tracking, click on the mouse button to the left.", True, font_color)
    line_6 = font.render(f"The number buttons let you choose how many fingers up are the signal to click!", True, font_color)
    line_7 = font.render(f"You can choose your play symbol and if a player is an AI in the sprites menu.", True, font_color)
    line_8 = font.render(f"If you actually took the time to read this, click on the sprites in the game over menus, who knows what might happen!", True, font_color)
    line_9 = font.render(f"Have fun!", True, font_color)

    line_1_rect = line_1.get_rect(center=(745 + totxsize//2+xoff, totysize//2 - 120+yoff))
    line_2_rect = line_2.get_rect(center=(745 + totxsize//2+xoff, totysize//2 - 90+yoff))
    line_3_rect = line_3.get_rect(center=(745 + totxsize//2+xoff, totysize//2 - 60+yoff))
    line_4_rect = line_4.get_rect(center=(745 + totxsize//2+xoff, totysize//2 - 30+yoff))
    line_5_rect = line_5.get_rect(center=(745 + totxsize//2+xoff, totysize//2 - 0+yoff))
    line_6_rect = line_6.get_rect(center=(745 + totxsize//2+xoff, totysize//2 + 30+yoff))
    line_7_rect = line_7.get_rect(center=(745 + totxsize//2+xoff, totysize//2 + 60+yoff))
    line_8_rect = line_8.get_rect(center=(745 + totxsize//2+xoff, totysize//2 + 90+yoff))
    line_9_rect = line_9.get_rect(center=(745 + totxsize//2+xoff, totysize//2 + 120+yoff))


    screen.blit(line_1, line_1_rect)
    screen.blit(line_2, line_2_rect)
    screen.blit(line_3, line_3_rect)
    screen.blit(line_4, line_4_rect)
    screen.blit(line_5, line_5_rect)
    screen.blit(line_6, line_6_rect)
    screen.blit(line_7, line_7_rect)
    screen.blit(line_8, line_8_rect)
    screen.blit(line_9, line_9_rect)

    #define t_anim
    t_anim = int(time.time()*10)
    
    #triggered by random event? 
    #bird test
    if t_anim%2 == 1:
        bird_fly = pygame.image.load(bird)
    else:
        bird_fly = pygame.image.load(bird[:-4]+'2.png')
    screen.blit(bird_fly,(-1500+20*(t_anim%500)+xoff, 100+yoff))
    
    
    #kitty test:
    if t_anim%2 == 1:
        cat_run = pygame.image.load(taby_cat)
    else:
        cat_run = pygame.image.load(taby_cat[:-4]+'_run.png')
    screen.blit(cat_run,(1500-10*(t_anim%200)+xoff, 650+yoff))
    
    
    
    #make the buttons appear 
    pos = pygame.mouse.get_pos()
    
    if exit_hitbox.collidepoint(pos):
        exit_img = pygame.image.load('images/exit_hover.png')
    else : 
        exit_img = pygame.image.load('images/exit.png')
    screen.blit(exit_img, (343.5+xoff, 707+yoff)) 

    if sound_hitbox.collidepoint(pos):
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2_selected.png')
    else : 
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2.png')
    screen.blit(sound_button, (709+xoff, 709+yoff))
    
    if darkmode: 
        darkmode_image = 'images/light_mode_v2.png'
    else: 
        darkmode_image = 'images/dark_mode_v2.png'
    if darkmode_hitbox.collidepoint(pos):
        darkmode_image = darkmode_image[:-4]+'_selected.png'
    darkmode_button = pygame.image.load(darkmode_image)
    screen.blit(darkmode_button, (709+xoff, 10+yoff))
    
    settings_img = 'images/settings' +('_hover.png' if settings_hitbox.collidepoint(pos) else '.png')
    screen.blit(pygame.image.load(settings_img), (10+xoff, yoff))

    #object tracking buttons 
    if nb_fingers == 0:
        zero_image = 'images/zero_clicked.png'
    else:
        zero_image = 'images/zero.png'
    if zero_hitbox.collidepoint(pos):
        zero_image = zero_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(zero_image), (105+xoff, 400+yoff))

    if nb_fingers == 1:
        one_image = 'images/one_clicked.png'
    else:
        one_image = 'images/one.png'
    if one_hitbox.collidepoint(pos):
        one_image = one_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(one_image), (205+xoff, 400+yoff))

    if nb_fingers == 2:
        two_image = 'images/two_clicked.png'
    else:
        two_image = 'images/two.png'
    if two_hitbox.collidepoint(pos):
        two_image = two_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(two_image), (305+xoff, 400+yoff))

    if nb_fingers == 3:
        three_image = 'images/three_clicked.png'
    else:
        three_image = 'images/three.png'
    if three_hitbox.collidepoint(pos):
        three_image = three_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(three_image), (405+xoff, 400+yoff))

    if nb_fingers == 4:
        four_image = 'images/four_clicked.png'
    else:
        four_image = 'images/four.png'
    if four_hitbox.collidepoint(pos):
        four_image = four_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(four_image), (505+xoff, 400+yoff))
    
    if select_mouse:
        mouse_image = 'images/mouse_clicked.png'
    else:
        mouse_image = 'images/mouse.png'
    if mouse_hitbox.collidepoint(pos):
        mouse_image = mouse_image[:-4]+'_hover.png'

    screen.blit(pygame.image.load(mouse_image), (605+xoff, 400+yoff))


    #make the background appear 
    if fullscreen: 
        if darkmode:
            background_img = "images/background_v2_nuit.png"
        else:
            background_img = "images/background_v2.png"
        infoObject = pygame.display.Info()
        screen.blit(pygame.image.load(background_img), ((infoObject.current_w - 2194)/2, (infoObject.current_h - 1080)/2))

    #handle events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            game = True
        elif event.type == pygame.K_q:
            done = True
            game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #buttons clicked -> consequences
            
            if exit_hitbox.collidepoint(pos):
                done = True    
                game = True 

            #object tracking buttons
            if zero_hitbox.collidepoint(pos):
                nb_fingers = 0

            if one_hitbox.collidepoint(pos):
                nb_fingers = 1
            
            if two_hitbox.collidepoint(pos):
                nb_fingers = 2

            if three_hitbox.collidepoint(pos):
                nb_fingers = 3

            if four_hitbox.collidepoint(pos):
                nb_fingers = 4

            if mouse_hitbox.collidepoint(pos):
                select_mouse = not select_mouse

            if sound_hitbox.collidepoint(pos):
                if sound_on : 
                    pygame.mixer.music.stop()
                    sound_on = False 
                else : 
                    sound_on = True
                    pygame.mixer.music.load(settings_music)
                    pygame.mixer.music.play(-1)
            
            if darkmode_hitbox.collidepoint(pos): 
                if darkmode: 
                    darkmode = False
                else: 
                    darkmode = True
    
            if settings_hitbox.collidepoint(pos): 
                in_settings = False
                if sound_on:
                    pygame.mixer.music.load(game_music)
                    pygame.mixer.music.play(-1)

    clock.tick(60)
        
    pygame.display.flip()

    return (done, game, in_menu, screen, fullscreen, offset, in_settings, nb_fingers, select_mouse)


def game_over_menu(game, done, game_over, in_menu, grid, TotalGrid, allowedx, allowedy, full_cases, screen, fullscreen, offset, TTG):
    """Draw the game over screen."""
    global darkmode
    global sound_on
    
    xoff, yoff = offset

    #make the button hitboxes
    exit_hitbox = pygame.Rect(343.5+xoff, 707+yoff, 58, 30)
    pygame.draw.rect(screen, [0,0,0], exit_hitbox) 

    yes_hitbox = pygame.Rect(306+xoff, 390+yoff, 44, 30) 
    pygame.draw.rect(screen, [0,0,0], yes_hitbox) 
    
    no_hitbox = pygame.Rect(395+xoff, 390+yoff, 44, 30)
    pygame.draw.rect(screen, [0,0,0], no_hitbox) 
    
    darkmode_hitbox = pygame.Rect(709+xoff, 10+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], darkmode_hitbox) 

    snake_hitbox = pygame.Rect(97+xoff, 483+yoff, 50, 50)
    pygame.draw.rect(screen, [0,0,0], snake_hitbox) 

    sushi_hitbox = pygame.Rect(338+xoff, 485+yoff, 60, 50)
    pygame.draw.rect(screen, [0,0,0], sushi_hitbox) 

    fullscreen_hitbox = pygame.Rect(10+xoff, 709+yoff, 28, 28)
    pygame.draw.rect(screen, [0,0,0], fullscreen_hitbox) 

    sound_hitbox = pygame.Rect(709+xoff, 709+yoff, 26, 26)
    pygame.draw.rect(screen, [0,0,0], sound_hitbox) 

    gmover_img = 'images/'+game_over #either 'p1_win', 'p2_win' or 'tie' 
    if darkmode: 
        gmover_img += '_nuit'
    gmover_img += '.png'

    screen.blit(pygame.image.load(gmover_img), (xoff, yoff))

    #make buttons appear
    pos = pygame.mouse.get_pos()

    if exit_hitbox.collidepoint(pos):
        exit_img = pygame.image.load('images/exit_hover.png')
    else : 
        exit_img = pygame.image.load('images/exit.png')
    screen.blit(exit_img, (343.5+xoff, 707+yoff)) 

    if yes_hitbox.collidepoint(pos):
        yes_img = pygame.image.load('images/yes_hover.png')
    else : 
        yes_img = pygame.image.load('images/yes.png')
    screen.blit(yes_img, (306+xoff, 390+yoff)) 
    
    if no_hitbox.collidepoint(pos):
        no_button = pygame.image.load('images/no_hover.png')
    else : 
        no_button = pygame.image.load('images/no.png')
    screen.blit(no_button, (395+xoff, 390+yoff))
    
    if darkmode: 
        darkmode_image = 'images/light_mode_v2.png'
    else: 
        darkmode_image = 'images/dark_mode_v2.png'
    if darkmode_hitbox.collidepoint(pos):
        darkmode_image = darkmode_image[:-4]+'_selected.png'
    darkmode_button = pygame.image.load(darkmode_image)
    screen.blit(darkmode_button, (709+xoff, 10+yoff))

    fullscreen_img = 'images/fullscreen' +('_on.png' if fullscreen else '.png')
    if fullscreen_hitbox.collidepoint(pos):
        fullscreen_img = fullscreen_img[:-4]+'_selected.png'
    screen.blit(pygame.image.load(fullscreen_img), (10+xoff, 709+yoff))

    if sound_hitbox.collidepoint(pos):
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2_selected.png')
    else : 
        sound_button = pygame.image.load('images/sound_'+('on' if sound_on else 'off')+'_v2.png')
    screen.blit(sound_button, (709+xoff, 709+yoff))

    #background 
    if fullscreen: 
        if darkmode:
            background_img = "images/background_nuit.png"
        else:
            background_img = "images/background.png"
        infoObject = pygame.display.Info()
        screen.blit(pygame.image.load(background_img), ((infoObject.current_w - 1920)/2, (infoObject.current_h - 1080)/2))

    #handle events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            game = True
        elif event.type == pygame.K_q:
            done = True
            game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            #buttons clicked -> consequences
            #collide in button creation (rectangle creation) to change appearance 

            if exit_hitbox.collidepoint(pos):
                done = True    
                game = True 

            if yes_hitbox.collidepoint(pos):
                in_menu = True
                game = False
                game_over = ''
                done = False
                grid = [[0 for _ in range(9)] for _ in range(9)] 
                TotalGrid = [[0 for _ in range(3)] for _ in range(3)]
                allowedx = -1 
                allowedy = -1
                ResizePlayBox(playrect,allowedx,allowedy, HEIGHT, WIDTH, offset)
                TTG = [['.' for _ in range(9)] for _ in range(9)]
                full_cases = 0 
                if sound_on:
                    pygame.mixer.music.load(theme)
                    pygame.mixer.music.play(-1)
                in_menu = True

                    
            if no_hitbox.collidepoint(pos):
                game_over = ''
                done = True

            if darkmode_hitbox.collidepoint(pos): 
                if darkmode: 
                    darkmode = False
                else: 
                    darkmode = True
            
            if (sound_on and (not darkmode) and game_over == 'p2_win'):
                if snake_hitbox.collidepoint(pos):
                    pygame.mixer.music.load('sounds/lwymmd.wav')
                    pygame.mixer.music.play(-1)

            if (sound_on and darkmode and game_over == 'tie'):
                if sushi_hitbox.collidepoint(pos):
                    pygame.mixer.music.load('sounds/megalovania.wav')
                    pygame.mixer.music.play(-1)

            if fullscreen_hitbox.collidepoint(pos): 
                if fullscreen: 
                    screen = pygame.display.set_mode(WINDOW_SIZE)
                    offset = (0, 0)
                else: 
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    infoObject = pygame.display.Info()
                    offset = ((infoObject.current_w-745)/2, (infoObject.current_h-745)/2)
                fullscreen = not fullscreen #becomes False if True, True if False 

            if sound_hitbox.collidepoint(pos):
                if sound_on : 
                    pygame.mixer.music.stop()
                    sound_on = False 
                else : 
                    sound_on = True
                    pygame.mixer.music.load(gameover_music)
                    pygame.mixer.music.play(-1)


    clock.tick(60)
        
    pygame.display.flip()

    return (game, done, game_over, in_menu, grid, TotalGrid, allowedx, allowedy, full_cases, screen, fullscreen, offset, TTG) 

