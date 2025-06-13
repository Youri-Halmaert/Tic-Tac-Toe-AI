# The heart of our code (first version)
import pygame
import time 
import os 

# Executing the interface 
from interface import * 
from minimax import *
from tcp_connect import *
from Test_code_handtracking import *

# Variables
in_menu = False
game = False #True if a button to start the game has been clicked 
last_move = (0, 0) # last move we played, when it changes communication can tell the other device 
p1_gamemode = "player" # default for now, will be able to change it in the interface later with the two buttons per player
p2_gamemode = "player" # same
redPlaying = True
in_settings = False # tells us if we're in the settings menu in game or not 
nb_fingers = 0 
select_mouse = True
clic = False 
width = 735 
height = 735
pos = [width/2, height/2]
box_won=['0', '0', '0', '0', '0', '0', '0', '0', '0']
possible_goals=[(0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 1, 2), (3, 4, 5), (6, 7, 8)]
bot_state='0'*81
bot_move=-1
#nb_move = 0
first_player = 0
difficulty = (1,1) #AI's difficulty level, in order for p1 AI and p2 AI
pseudo = socket.gethostname() #get the hostname for a pseudo by default
pseudo_adv = socket.gethostname()
ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]][0] #get the ip address
port = "1234"
valid = False
connection = False
played = False
online = False
connect = False
sound_on = False
TTG = [["." for i in range(9)] for j in range(9)] #state of play for the communication

# Functions 
def winSetter(OC,Team,grid,TotalGrid, game_over):
    global full_cases 

    TotalGrid[OC[0]//3][OC[1]//3] = Team
    for x in range((OC[0]//3) * 3,(OC[0]//3) *3 + 3):
        for y in range((OC[1]//3) * 3,(OC[1]//3) *3 + 3):
            grid[x][y] = Team
    for x in range(0,3):
        if TotalGrid[x][0] == Team and TotalGrid[x][1] == Team and TotalGrid[x][2] == Team:
            if Team == 1:
                #SetWin(Grid,1,TotalGrid)
                game_over = 'p1_win'
                if sound_on:
                    pygame.mixer.music.load(gameover_music)
                    pygame.mixer.music.play(-1)
            else:
                #SetWin(Grid,2,TotalGrid)
                game_over = 'p2_win'
                if sound_on:
                    pygame.mixer.music.load(gameover_music)
                    pygame.mixer.music.play(-1)
    for y in range(0,3):
        if TotalGrid[0][y] == Team and TotalGrid[1][y] == Team and TotalGrid[2][y] == Team:
            if Team == 1:
                #SetWin(Grid,1,TotalGrid)
                game_over = 'p1_win'
                if sound_on:
                    pygame.mixer.music.load(gameover_music)
                    pygame.mixer.music.play(-1)
            else:
                #SetWin(Grid,2,TotalGrid)
                game_over = 'p2_win'
                if sound_on:
                    pygame.mixer.music.load(gameover_music)
                    pygame.mixer.music.play(-1)
    if (TotalGrid[0][0] ==Team and TotalGrid[1][1] == Team and TotalGrid[2][2] == Team) or (TotalGrid[2][0] == Team and TotalGrid[1][1] == Team and TotalGrid[0][2] == Team ):
        if Team == 1:
            #SetWin(Grid,1,TotalGrid)
            game_over = 'p1_win'
            if sound_on:
                    pygame.mixer.music.load(gameover_music)
                    pygame.mixer.music.play(-1)
        else:
            #SetWin(Grid,2,TotalGrid)
            game_over = 'p2_win'
            if sound_on:
                    pygame.mixer.music.load(gameover_music)
                    pygame.mixer.music.play(-1)
    full_cases +=1 
    if full_cases == 9:
        game_over = 'tie'
        if sound_on:
            pygame.mixer.music.load(gameover_music)
            pygame.mixer.music.play(-1)
    return game_over

def winCalc(OuterCords,Grid,TotalGrid, game_over):
    global full_cases 

    OC = OuterCords
    IC = (OC[0]%3,OC[1]%3)
    thisTileTeam = Grid[OC[0]][OC[1]]
    Team = thisTileTeam
    if thisTileTeam == 0:
        return "Invalid Team"
    if IC == (0,0):

        if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]+2][OC[1]] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]+2] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]+1][OC[1]+1] == thisTileTeam and Grid[OC[0]+2][OC[1]+2] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
    elif IC == (1,0):
        if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]-1][OC[1]] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]+2] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
    elif IC == (2,0):
        if Grid[OC[0]-1][OC[1]] == thisTileTeam and Grid[OC[0]-2][OC[1]] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]+2] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]-1][OC[1]+1] == thisTileTeam and Grid[OC[0]-2][OC[1]+2] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
    elif IC == (0,1):
        if Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]-1] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]+2][OC[1]] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
    elif IC == (1,1):
        if Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]-1] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]-1][OC[1]] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]-1][OC[1]-1] == thisTileTeam and Grid[OC[0]+1][OC[1]+1] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]-1][OC[1]+1] == thisTileTeam and Grid[OC[0]+1][OC[1]-1] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)

    elif IC == (2,1):
        if Grid[OC[0]][OC[1]+1] == thisTileTeam and Grid[OC[0]][OC[1]-1] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]-1][OC[1]] == thisTileTeam and Grid[OC[0]-2][OC[1]] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)

    elif IC == (0,2):
        if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]+2][OC[1]] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]][OC[1]-1] == thisTileTeam and Grid[OC[0]][OC[1]-2] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]+1][OC[1]-1] == thisTileTeam and Grid[OC[0]+2][OC[1]-2] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
    elif IC == (1,2):
        if Grid[OC[0]+1][OC[1]] == thisTileTeam and Grid[OC[0]-1][OC[1]] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]][OC[1]-1] == thisTileTeam and Grid[OC[0]][OC[1]-2] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)

    elif IC == (2,2):
        if (Grid[OC[0]][OC[1]-1] == thisTileTeam and Grid[OC[0]][OC[1]-2] == thisTileTeam) :
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif (Grid[OC[0]-1][OC[1]] == thisTileTeam and Grid[OC[0]-2][OC[1]] == thisTileTeam):
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
        elif Grid[OC[0]-1][OC[1]-1] == thisTileTeam and Grid[OC[0]-2][OC[1]-2] == thisTileTeam:
            game_over = winSetter(OC,thisTileTeam,Grid,TotalGrid, game_over)
    amtused = 0
    for x in range(OC[0]-IC[0],OC[0]-IC[0]+3):
        for y in range(OC[1]-IC[1],OC[1]-IC[1]+3):
            if Grid[x][y] != 0:
                amtused = amtused + 1
    if amtused == 9:
        if TotalGrid[OC[0]//3][OC[1]//3] == 0:
            TotalGrid[OC[0]//3][OC[1]//3] = -1
            full_cases += 1 
            if full_cases == 9:
                game_over = 'tie'
                if sound_on:
                    pygame.mixer.music.load(gameover_music)
                    pygame.mixer.music.play(-1)
    return game_over 

def player_mode(game_over, played, grid, TotalGrid, HEIGHT, WIDTH, offset, in_settings): 
    """The gamemode for a human player. The player can click on the grid."""
    global redPlaying 
    global darkmode 
    global allowedx
    global allowedy
    global last_move
    global select_mouse
    global clic
    global pos
    global nb_fingers

    xoff, yoff = offset
    clic = False
    
    if not select_mouse:
        rect = [playrect[0] - 5 - xoff, playrect[1] - 5 - yoff, playrect[2] - 5, playrect[3]-5]
        pos, clic = handtracking(rect, pos ,clic, nb_fingers)
        pos = [pos[0]+ xoff, pos[1] + yoff]
    else:
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN :
            clic = True
    
    if clic: 
        if pos[0]-xoff < 50 and pos[0]-xoff > 10 and pos[1]-yoff < 10 and pos[1]-yoff > 0 :
            in_settings = True
        
        elif pos[0]-xoff > 10 and pos[0]-xoff < 735 and pos[1]-yoff > 10 and pos[1]-yoff < 735:
            xcord = int(((pos[0]-xoff - (((pos[0]-xoff)//tot3by3)-1)*MARGIN) - 2*MARGIN) // (MARGIN+WIDTH))
            ycord = int(((pos[1]-yoff - (((pos[1]-yoff)//tot3by3)-1)*MARGIN) - 2*MARGIN)// (MARGIN+HEIGHT))
            
            if xcord /8 <= 1 and ycord /8 <= 1: 
                if grid[xcord][ycord] == 0:
                    if allowedx == -1 and allowedy == -1: #move anywhere
                        
                        last_move = (xcord, ycord)

                        if redPlaying == True: 
                            grid[xcord][ycord] = 1
                            redPlaying = False
                        else: #same here 
                            grid[xcord][ycord] = 2 
                            redPlaying = True
                        game_over = winCalc([xcord,ycord],grid,TotalGrid, game_over)
                        allowedx ,allowedy = NextBox([xcord,ycord],TotalGrid)
                        ResizePlayBox(playrect,allowedx,allowedy, HEIGHT, WIDTH, offset)
                        played = True

                    elif allowedx <= xcord <= allowedx+2 and allowedy <= ycord <= allowedy+2:
                        last_move = (xcord, ycord)
                        if redPlaying == True:
                            grid[xcord][ycord] = 1
                            redPlaying = False

                        else:
                            grid[xcord][ycord] = 2
                            redPlaying = True
                        game_over = winCalc([xcord,ycord],grid,TotalGrid, game_over)
                        allowedx ,allowedy = NextBox([xcord,ycord],TotalGrid)
                        ResizePlayBox(playrect,allowedx,allowedy, HEIGHT, WIDTH, offset)
                        played = True

    return (game_over, played, grid, TotalGrid, last_move, in_settings, allowedx, allowedy, redPlaying)

def ai_move(last_move,game_over,grid,TotalGrid,redPlaying, HEIGHT, WIDTH, offset,bot_state,bot_move,indice_player,indice_bot):
    global box_wonglobal, possible_goals, first_player
    
    if redPlaying:
        depth= 2+difficulty[0]
    if not redPlaying:
        first_player = 1
        depth = 2+difficulty[1]

    #prise coup joueur si il y en a un
    if (p1_gamemode=="player" or p2_gamemode=="player" or p1_gamemode=="other" or p2_gamemode=="other") and first_player == 1:
        user_state,user_move=joueur(bot_state,bot_move,last_move,indice_player)
        #nb_move += 1

    else:
        first_player = 1
        user_move=bot_move
        user_state=bot_state
        
    #ia
    
    #if nb_move >= 45:
    #   depth += 1 
    #can be better on more performant devices
    
    bot_state,bot_move=bot(user_state,user_move,indice_bot,depth)
    #nb_move += 1
    raw,col=translate(bot_move)
    xcord=col
    ycord=raw
    last_move=col,raw

    if p1_gamemode == "ai" and redPlaying:
        redPlaying = False
        grid[xcord][ycord] = 1
    else:
        redPlaying = True
        grid[xcord][ycord] = 2

    game_over = winCalc([xcord, ycord], grid, TotalGrid, game_over)
    allowedx, allowedy = NextBox([xcord, ycord], TotalGrid)
    ResizePlayBox(playrect, allowedx, allowedy, HEIGHT, WIDTH, offset)

    return(last_move,bot_move, bot_state, game_over, grid, TotalGrid,redPlaying,allowedx, allowedy)


    #AI mode: AI chooses xcord and ycord directly and we ignore clicks on boxes, updates who's playing and the grids 
    #you'll need to check imports, I haven't been able to do it yet 


# Main code: 
pygame.mixer.music.load(start_music)
pygame.mixer.music.play(-1)

while not in_menu:
    done, game, in_menu, screen, fullscreen, offset, nb_fingers, select_mouse = start_menu(done, game, in_menu, screen, fullscreen, offset, nb_fingers, select_mouse)

while not done:
    if not game : 
        if in_menu :
            done, game, in_menu, screen, online, fullscreen, offset = menu(done, game, in_menu, screen, online, fullscreen, offset)
        elif connect:
            if p1_gamemode == "other": #we select host
                if connection:
                    waiting_screen(offset)
                    code, pseudo_adv, sock = connect_P1(ip, int(port), pseudo)
                    match code:
                        case 0:
                            game = True
                        case _:
                            game = True
                            game_over = "error"

                done, game, in_menu, screen, pseudo, connection, connect, fullscreen, offset, (p1_gamemode, p2_gamemode) = host_connect(done, game, in_menu, screen, ip, port, pseudo, valid, connection, connect, fullscreen, offset, (p1_gamemode, p2_gamemode))
                if re.match("[a-zA-Z0-9]+", pseudo):
                    valid = True
                else :
                    valid = False

            else: #we select guest
                if connection:
                    waiting_screen(offset)
                    code, pseudo_adv, sock = connect_P2(ip, int(port), pseudo)
                    match code:
                        case 0:
                            game = True
                        case _:
                            game = True
                            game_over = "error"

                done, game, in_menu, screen, ip, port, pseudo, connection, connect, fullscreen, offset, (p1_gamemode, p2_gamemode) = guest_connect(done, game, in_menu, screen, ip, port, pseudo, valid, connection, connect, fullscreen, offset, (p1_gamemode, p2_gamemode))
                if not re.match("[a-zA-Z0-9]+", pseudo):
                    valid = False
                elif not re.match("(\d{1,3}\.){3}\d{1,3}$", ip):
                    valid = False
                elif not re.match("[0-9]+", port):
                    valid = False
                elif int(port)< 1024:
                    valid = False
                else :
                    valid = True

        elif online:
            done, game, in_menu, screen, connect, fullscreen, offset, (p1_gamemode, p2_gamemode)  = online_select(done, game, in_menu, screen, connect, fullscreen, offset, (p1_gamemode, p2_gamemode))
        
        else : 
            done, game, in_menu, screen, fullscreen, offset, (p1_gamemode, p2_gamemode), difficulty  = sprite_menu(done, game, in_menu, screen, fullscreen, offset, (p1_gamemode, p2_gamemode), difficulty)
    
        
        #handling the screen size change when entering the game 
        if game:
            fullscreen = True 
            screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            infoObject = pygame.display.Info()
            offset = ((infoObject.current_w - 2194)/2+352, (infoObject.current_h - 1080)/2+168)
            ResizePlayBox(playrect,allowedx,allowedy, HEIGHT, WIDTH, offset)

    
    else:
        if game_over=='': #no game over yet 
            if in_settings: 
                (done, game, in_menu, screen, fullscreen, offset, in_settings, nb_fingers, select_mouse) = settings_menu(done, game, in_menu, screen, fullscreen, offset, in_settings, nb_fingers, select_mouse)
            else:
                done, last_move, game_over, grid, TotalGrid, HEIGHT, WIDTH, offset, in_settings = game_menu(done, last_move, game_over, grid, TotalGrid, offset, fullscreen, allowedx, allowedy, in_settings, redPlaying, online, pseudo, pseudo_adv, (p1_gamemode, p2_gamemode)) 
                
                if ((p1_gamemode == "ai" and redPlaying) or (p2_gamemode =="ai" and not redPlaying)) :
                    indice_player, indice_bot=who_is_player(redPlaying)
                    last_move,bot_move, bot_state, game_over, grid, TotalGrid,redPlaying,allowedx, allowedy=ai_move(last_move,game_over,grid,TotalGrid,redPlaying, HEIGHT, WIDTH, offset,bot_state,bot_move,indice_player,indice_bot)
                    xcord, ycord = last_move
                    big_game = xcord // 3 +(ycord // 3) * 3
                    mini_game = xcord % 3 + (ycord % 3) * 3
                    if online:
                        code, TTG = play(sock, big_game, mini_game, TTG, redPlaying)
                        match code:
                            case 0:
                                pass
                            case _:
                                game_over = "error" 
                    continue
                                
                elif ((p1_gamemode == "other" and redPlaying) or (p2_gamemode =="other" and not redPlaying)) : 
                    code, TTG, big_game, mini_game, pseudo = new_state(sock, TTG, pseudo, redPlaying)
                    match code:
                        case 0:
                            xcord = 3 * (big_game %3) + (mini_game % 3)
                            ycord = 3 * (big_game // 3) + (mini_game // 3)

                            if redPlaying == True:
                                grid[xcord][ycord] = 1
                                playcolour = ((255,255,0) if darkmode else (0,255,0))
                                redPlaying = False

                            else: #same here
                                grid[xcord][ycord] = 2
                                playcolour = ((0, 255, 255) if darkmode else (255,0,0))
                                redPlaying = True
                            game_over = winCalc([xcord,ycord],grid,TotalGrid, game_over)
                            allowedx ,allowedy = NextBox([xcord,ycord],TotalGrid)
                            ResizePlayBox(playrect,allowedx,allowedy, HEIGHT, WIDTH, offset)
                            last_move = xcord, ycord
                        case 4: #win detected or there isn't
                            fatal_error(sock)
                            close(sock)
                            game_over = "error"
                        case _:
                            game_over = "error" 
                    continue
                            
                elif not select_mouse and ( ((p1_gamemode == "player" and redPlaying) or (p2_gamemode =="player" and not redPlaying)) ):
                    game_over, played, grid, TotalGrid, last_move, in_settings, allowedx, allowedy, redPlaying = player_mode(game_over, played, grid, TotalGrid, HEIGHT, WIDTH, offset, in_settings)
                    xcord, ycord = last_move
                    big_game = xcord // 3 +(ycord // 3) * 3
                    mini_game = xcord % 3 + (ycord % 3) * 3
                    if online and played:
                        code, TTG = play(sock, big_game, mini_game, TTG, redPlaying)
                        match code:
                            case 0:
                                pass
                            case _:
                                game_over = "error"
                    played = False
                    continue

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    elif event.type == pygame.K_q:
                        done = True

                    elif ((p1_gamemode == "player" and redPlaying) or (p2_gamemode =="player" and not redPlaying)) : 
                        game_over, played, grid, TotalGrid, last_move, in_settings, allowedx, allowedy, redPlaying = player_mode(game_over, played, grid, TotalGrid, HEIGHT, WIDTH, offset, in_settings) 
                        xcord, ycord = last_move
                        big_game = xcord // 3 +(ycord // 3) * 3
                        mini_game = xcord % 3 + (ycord % 3) * 3
                        if online and played:
                            code, TTG = play(sock, big_game, mini_game, TTG, redPlaying)
                            match code:
                                case 0:
                                    pass
                                case _:
                                    game_over = "error"
                        played = False
                    
                if in_settings and sound_on:
                    pygame.mixer.music.load(settings_music)
                    pygame.mixer.music.play(-1)

            #handling going into the game over screen 
            if game_over != '':
                screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                infoObject = pygame.display.Info()
                offset = ((infoObject.current_w-745)/2, (infoObject.current_h-745)/2)



        else: #error, p1_win, p2_win or tie 
            if game_over == "error":
                error_screen(offset)
                continue
            if online:
                if ((p1_gamemode == "other" and redPlaying) or (p2_gamemode =="other" and not redPlaying)) :
                    code, TTG, big_game, mini_game, pseudo = new_state(sock, TTG, pseudo, redPlaying)
                    match code:
                        case 0:
                            pass
                        case 4: #win detected or there isn't
                            end(sock)
                        case _:
                            game_over = "error"
                else:
                    code = win(sock, game_over)
                    match code :
                        case 0:
                            pass
                        case _:
                            game_over = "error"

            #reinit the variables
            online = False
            connect = False
            connection = False
            p1_gamemode = "player"
            p2_gamemode = "player"
            box_won = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
            possible_goals = [(0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 1, 2), (3, 4, 5), (6, 7, 8)]
            bot_state = '0' * 81
            bot_move = -1
            first_player = 0
            nb_move = 0
            infoObject = pygame.display.Info()
            offset = ((infoObject.current_w-745)/2, (infoObject.current_h-745)/2)
            redPlaying = True 

            game, done, game_over, in_menu, grid, TotalGrid, allowedx, allowedy, full_cases, screen, fullscreen, offset, TTG = game_over_menu(game, done, game_over, in_menu, grid, TotalGrid, allowedx, allowedy, full_cases, screen, fullscreen, offset, TTG)
            

pygame.quit()




