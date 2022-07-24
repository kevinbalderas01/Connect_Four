import numpy as np
import pygame
import sys
ROWS = 6
COLUMNS = 7
board= np.zeros((ROWS, COLUMNS))
image = pygame.image.load('pop.png')

SLOT = 100
WIDTH = COLUMNS * SLOT
HEIGHT = (ROWS +1) * SLOT
SIZE = (WIDTH, HEIGHT)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
GRAY = (127,127,127)
OFFSET = 100
RADIUS = (SLOT//2) - 5

def draw_board(board, window):
    #Draw the gray rectangle, space for moving piece
    pygame.draw.rect(window, GRAY, (0,0,WIDTH, SLOT))
    #Draw the empty pieces on the board
    for c in range(COLUMNS):
        for r in range(ROWS):
            rect = (c*SLOT, r*SLOT + OFFSET, SLOT, SLOT)
            center = (int(c*SLOT + (SLOT //2)), int(r*SLOT + OFFSET + (SLOT //2)))
            pygame.draw.rect(window, BLUE, rect)
            pygame.draw.circle(window, BLACK, center, RADIUS)
    #Draw the pieces landed by the players
    for c in range(COLUMNS):
        for r in range(ROWS):
            center_pl = (int(c*SLOT + (SLOT //2)), HEIGHT - int(r*SLOT + (SLOT //2)))
            if board[r][c] == 1:
                pygame.draw.circle(window, GREEN, center_pl, RADIUS)
            elif board[r][c]==2:
                pygame.draw.circle(window, RED, center_pl, RADIUS)
    pygame.display.update()


def is_valid_location(board, col):
    #When a single column is filled with pieces
    return board[ROWS-1][col] ==0

def drop_piece(board, col, piece):
    for r in range(ROWS):
        if board[r][col] == 0:
            row = r
            break
    board[r][col] = piece

def is_wining_move(board, piece):
    #Check horizontal locations to win
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3]== piece:
                return True
    #Check verticals locations to win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c]== piece:
                return True
    #Check possitive diagonals location to win
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3]== piece:
                return True
    #Check negative diagonals location to win
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3]== piece:
                return True

def main():
    game_over = False
    turn = 0
    pygame.init()
    window = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("CONNECT4")
    font = pygame.font.SysFont("Comic Sans MS", 33, True)
    draw_board(board, window)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEMOTION:
                #Fill the old space so we see nothing has changed
                pygame.draw.rect(window, GRAY, (0,0, WIDTH, SLOT))
                posx = event.pos[0]
                if turn % 2 == 0:
                    pygame.draw.circle(window, GREEN, (((posx//SLOT)*SLOT + (SLOT //2)), SLOT//2), RADIUS)

                else:
                    pygame.draw.circle(window, RED, (((posx//SLOT)*SLOT + (SLOT //2)), SLOT//2), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(event.pos[0] // SLOT)
                if turn % 2 == 0:
                    col = event.pos[0] // SLOT
                    if is_valid_location(board, col):
                        drop_piece(board, col, 1)
                        if is_wining_move(board,1):
                            #print("WON 1")
                            label = font.render("Player 1 WON !!!", True, GREEN)
                            game_over = True
                    else:
                        turn -= 1
                else:
                    col = event.pos[0] // SLOT
                    if is_valid_location(board, col):
                        drop_piece(board, col, 2)
                        if is_wining_move(board,2):
                            #print("WON P2")
                            label = font.render("Player 2 WON !!!", True, RED)
                            game_over = True
                    else:
                        turn -= 1
                turn +=1
                print(np.flip(board,0))
                draw_board(board, window)
            if game_over:
                window.blit(image, (120,220))
                window.blit(label, (170, 350))
                pygame.display.update()
                pygame.time.wait(3000)


if __name__ == '__main__':
    main()
