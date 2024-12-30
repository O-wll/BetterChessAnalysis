import pygame
import ChessPieces

class Chessboard:
    pass

def generate_board():  # Generates the chessboard and the pieces in starting position.

    # Variables used in chessboard generation
    CHESS_ROWS = 8
    xCoordinate = 0
    yCoordinate = 0

    pygame.init()  # Initiate pygame function/methods.

    # Pieces
    screen = pygame.display.set_mode((1000, 800))
    darkSquare = pygame.image.load("images/ChessDarkSquare.png").convert()
    lightSquare = pygame.image.load("images/ChessLightSquare.png").convert()
    whiteRook = pygame.image.load("images/ChessRookWhite.png").convert()
    blackRook = pygame.image.load("images/ChessRookBlack.png").convert()

    for index in range(CHESS_ROWS):
        for i in range(8):
            if index % 2 == 0:
                screen.blit(lightSquare, (xCoordinate, yCoordinate))
            else:
                screen.blit(darkSquare, (xCoordinate, yCoordinate))
            index += 1
            xCoordinate += 64

        xCoordinate = 0
        yCoordinate += 64

    pygame.display.flip()
