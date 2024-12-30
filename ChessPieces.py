import pygame

pygame.init()  # Initiate pygame function/methods.
screen = pygame.display.set_mode((1000, 800))


class ChessPieces:
    def __init__(self, color, piece_type):
        self.piece_type = piece_type
        self.color = color


def get_white_rook():
    whiteRook = pygame.image.load("images/ChessRookWhite.png").convert_alpha()
    whiteRook = pygame.transform.scale(whiteRook, (48, 48))

    return whiteRook


def get_black_rook():
    blackRook = pygame.image.load("images/ChessRookBlack.png").convert_alpha()
    blackRook = pygame.transform.scale(blackRook, (48, 48))

    return blackRook


def get_white_knight():
    whiteKnight = pygame.image.load("images/ChessKnightWhite.png").convert_alpha()
    whiteKnight = pygame.transform.scale(whiteKnight, (48, 48))

    return whiteKnight


def get_black_knight():
    blackKnight = pygame.image.load("images/ChessKnightBlack.png").convert_alpha()
    blackKnight = pygame.transform.scale(blackKnight, (48, 48))

    return blackKnight


def get_white_bishop():
    whiteBishop = pygame.image.load("images/ChessBishopWhite.png").convert_alpha()
    whiteBishop = pygame.transform.scale(whiteBishop, (48, 48))

    return whiteBishop


def get_black_bishop():
    blackBishop = pygame.image.load("images/ChessBishopBlack.png").convert_alpha()
    blackBishop = pygame.transform.scale(blackBishop, (48, 48))

    return blackBishop


def get_white_pawn():
    whitePawn = pygame.image.load("images/ChessPawnWhite.png").convert_alpha()
    whitePawn = pygame.transform.scale(whitePawn, (48, 48))

    return whitePawn


def get_black_pawn():
    blackPawn = pygame.image.load("images/ChessPawnBlack.png").convert_alpha()
    blackPawn = pygame.transform.scale(blackPawn, (42, 42))

    return blackPawn


def get_white_king():
    whiteKing = pygame.image.load("images/ChessKingWhite.png").convert_alpha()
    whiteKing = pygame.transform.scale(whiteKing, (48, 48))

    return whiteKing


def get_black_king():
    blackKing = pygame.image.load("images/ChessKingBlack.png").convert_alpha()
    blackKing = pygame.transform.scale(blackKing, (48, 48))

    return blackKing


def get_white_queen():
    whiteQueen = pygame.image.load("images/ChessQueenWhite.png").convert_alpha()
    whiteQueen = pygame.transform.scale(whiteQueen, (48, 48))

    return whiteQueen


def get_black_queen():
    blackQueen = pygame.image.load("images/ChessQueenBlack.png").convert_alpha()
    blackQueen = pygame.transform.scale(blackQueen, (48, 48))

    return blackQueen


class generate_pieces(ChessPieces):
    def make_piece(self):
        if self.color == "White" and self.piece_type == "Rook":
            return get_white_rook()
        elif self.color == "Black" and self.piece_type == "Rook":
            return get_black_rook()
        elif self.color == "White" and self.piece_type == "Knight":
            return get_white_knight()
        elif self.color == "Black" and self.piece_type == "Knight":
            return get_black_knight()
        elif self.color == "White" and self.piece_type == "Bishop":
            return get_white_bishop()
        elif self.color == "Black" and self.piece_type == "Bishop":
            return get_black_bishop()
        elif self.color == "White" and self.piece_type == "Pawn":
            return get_white_pawn()
        elif self.color == "Black" and self.piece_type == "Pawn":
            return get_black_pawn()
        elif self.color == "White" and self.piece_type == "King":
            return get_white_king()
        elif self.color == "Black" and self.piece_type == "King":
            return get_black_king()
        elif self.color == "White" and self.piece_type == "Queen":
            return get_white_queen()
        elif self.color == "Black" and self.piece_type == "Queen":
            return get_black_queen()
