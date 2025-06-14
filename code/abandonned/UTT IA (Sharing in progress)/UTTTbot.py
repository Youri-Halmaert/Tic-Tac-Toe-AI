import pygame
import os
import sys
import random
import time
from Board import new_Board

from Frontend import fill
from Frontend import Draw_pieces
from Frontend import draw_board
from Frontend import draw_big_pieces

from Check_game import Check_horizontally, Check_vertically, Check_diagonals, Check_Big_Board, empty_cells_big_board, Check_empty_cells
from Check_game import get_possible_moves
from Check_game import Validate_box
from Check_game import valid_locations, set_locations
from Check_game import check_game

from minimax import Minimax



pygame.font.init()

Width, Height = 810,810
Square = Width//3
Small_Square = Square//3
margin = Width//30

Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Ultimate Tic Tac Toe")
clock = pygame.time.Clock()

Cross_small = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "cross.png")), (Small_Square, Small_Square))
Cross = pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'cross.png')), (Square, Square))

Circle_small = pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'circle.png')), (Small_Square, Small_Square))
Circle = pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'circle.png')), (Square, Square))

Bg = (0,0,0)
Lines_color = (211,211,211)
Lines_color_2 = (250, 0, 0)

Game_Board = new_Board()


def update_window(Win, Lines_color, Lines_color_2, Width, Square, Small_Square, margin, Small_Cross, Small_Circle, Cross, Circle,board,big_board, player):
    Win.fill(Bg)
    Draw_pieces(Win,Small_Cross, Small_Circle,Cross, Circle, Small_Square, Square, board)
    draw_board(Win, Lines_color, Lines_color_2,Width, Square, Small_Square, margin)
    draw_big_pieces(Win, big_board, Square, Circle, Cross)
    pygame.display.update()


def main():
    run = True
    turn = random.choice([-1,1])
    AI1 = 1
    AI2 = -1
    #Game_Board.test()

    FPS = 120
    green = (0,178,0,0)
    game_over = False
    good = False


    box = None

    main_board = Game_Board.create_board()
    small_boards = Game_Board.every_small_boards()

    while run:

        clock.tick(FPS)
        fill(Circle_small,green)
        fill(Circle, green)
        update_window(Win, Lines_color, Lines_color_2, Width, Square, Small_Square, margin, Cross_small, Circle_small, Cross, Circle, small_boards, main_board, turn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if game_over:
                if game_over:
                    Game_Board.reset(small_boards, main_board, game_over)
                    game_over = False

        if turn == AI1 and not game_over:
            Depth = 3
            new_Board,value, pos = Minimax(small_boards, main_board,Depth, box,turn, True)
            small_boards = new_Board
            #print("pos",pos[0]//(Small_Square), pos[1]//(Small_Square))
            check_game(small_boards, main_board,turn)
            new_box = get_possible_moves(small_boards,pos[0], pos[1])
            #print("box after get_possible_moves", new_box)
            box = Validate_box(small_boards, main_board, new_box,pos[0], pos[1])
            #print("Box validated", box)

            #print("small_boards", small_boards)
            time.sleep(1)
            if Check_Big_Board(main_board, turn):
                game_over = True
                print("Circle Win")
            turn = AI2
        if turn == AI2:
            #print("in AI")
            Depth = 3
            new_Board,value, pos = Minimax(small_boards, main_board,Depth, box,turn, True)
            #print("Board, value, pos", new_Board,value, pos)
            small_boards = new_Board
            check_game(small_boards,main_board,turn)

            new_box = get_possible_moves(small_boards,pos[0], pos[1])
            box = Validate_box(small_boards, main_board, new_box,pos[0], pos[1])

            time.sleep(1)
            if Check_Big_Board(main_board, turn):
                game_over = True
                print("Cross win")
            turn = AI1



main()