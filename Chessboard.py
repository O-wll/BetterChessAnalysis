import pygame
import ChessPieces


class Chessboard:
    pass


def generate_board():  # Generates the chessboard and the pieces in starting position.
    pygame.init()  # Initiate pygame function/methods.

    # Variables used in chessboard generation
    CHESS_ROWS = 8
    xCoordinate = 0
    yCoordinate = 0

    # Pieces
    screen = pygame.display.set_mode((512, 512))
    darkSquare = pygame.image.load("images/ChessDarkSquare.png").convert()
    lightSquare = pygame.image.load("images/ChessLightSquare.png").convert()

    chessBoardPositions = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]

    pieceImage = {
        "wR": ChessPieces.generate_pieces("White", "Rook").make_piece(),
        "bR": ChessPieces.generate_pieces("Black", "Rook").make_piece(),
        "wN": ChessPieces.generate_pieces("White", "Knight").make_piece(),
        "bN": ChessPieces.generate_pieces("Black", "Knight").make_piece(),
        "wB": ChessPieces.generate_pieces("White", "Bishop").make_piece(),
        "bB": ChessPieces.generate_pieces("Black", "Bishop").make_piece(),
        "wQ": ChessPieces.generate_pieces("White", "Queen").make_piece(),
        "bQ": ChessPieces.generate_pieces("Black", "Queen").make_piece(),
        "wK": ChessPieces.generate_pieces("White", "King").make_piece(),
        "bK": ChessPieces.generate_pieces("Black", "King").make_piece(),
        "wP": ChessPieces.generate_pieces("White", "Pawn").make_piece(),
        "bP": ChessPieces.generate_pieces("Black", "Pawn").make_piece()
    }

    # Chessboard generation
    for row in range(CHESS_ROWS):
        for column in range(8):
            if row % 2 == 0:
                screen.blit(lightSquare, (xCoordinate, yCoordinate))
            else:
                screen.blit(darkSquare, (xCoordinate, yCoordinate))
            row += 1
            xCoordinate += 64

        xCoordinate = 0
        yCoordinate += 64

    yCoordinate = 0

    # Chess piece generation
    for row in range(CHESS_ROWS):
        for column in range(8):
            piece = chessBoardPositions[row][column]
            if piece:
                screen.blit(pieceImage[piece], ((xCoordinate + (64 * column)) + 6, (yCoordinate + (64 * row)) + 6))

    # screen.blit(piece, (xCoordinate + 5, yCoordinate + 5))
    pygame.display.flip()
