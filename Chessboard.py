import pygame
import ChessPieces


class Chessboard:
    pass


def generate_board():  # Generates the chessboard and the pieces in starting position.
    pygame.init()  # Initiate pygame function/methods.

    CHESS_ROWS = 8

    # Loading chess board
    screen = pygame.display.set_mode((512, 800))
    darkSquare = pygame.image.load("images/ChessDarkSquare.png").convert()
    lightSquare = pygame.image.load("images/ChessLightSquare.png").convert()
    selectHighlight = pygame.Surface((64, 64))
    selectHighlight.set_alpha(128)  # Transparency
    selectHighlight.fill((0, 255, 0))  # Green color

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

    chessNotation = [
        ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
        ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
        ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
        ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
        ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
        ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
        ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
        ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"],
    ]
    pieceNotation = ["R", "N", "B", "Q", "K"]
    chessActions = ["x", "+", "#", "e.p"]

    def render_board():
        xCoordinate = 0
        yCoordinate = 0

        # Draw the chessboard
        for row in range(CHESS_ROWS):
            for column in range(8):
                square = lightSquare if (row + column) % 2 == 0 else darkSquare
                screen.blit(square, (xCoordinate, yCoordinate))
                xCoordinate += 64
            xCoordinate = 0
            yCoordinate += 64

        # Draw the chess pieces
        for row in range(CHESS_ROWS):
            for column in range(8):
                piece = chessBoardPositions[row][column]
                if piece:
                    screen.blit(pieceImage[piece], (column * 64 + 6, row * 64 + 6))

        pygame.display.flip()

    render_board()  # Initial render of the board and pieces

    running = True
    selected_piece = None
    selected_coords = None
    player_turn = "w"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # TODO: Specify MOUSEBUTTONDOWN to be Mouse 1.
                xCoordinate, yCoordinate = event.pos
                # Divide by 64 to get good coord system (if at (64,64), coord will be (1,1))
                row = yCoordinate // 64
                column = xCoordinate // 64

                if selected_piece:  # If there is a piece selected, check to see if user clicks on same square.
                    if selected_coords == (row, column):
                        selected_piece = None
                        selected_coords = None

                if selected_piece:  # If player tries to make invalid move, reset coords and selected piece
                    if (row, column) not in valid_moves(selected_piece, chessBoardPositions, selected_coords):
                        selected_piece = None
                        selected_coords = None

                if selected_piece:  # Move the piece to the square then update
                    if (row, column) in valid_moves(selected_piece, chessBoardPositions, selected_coords):
                        chessBoardPositions[row][column] = selected_piece
                        chessBoardPositions[selected_coords[0]][selected_coords[1]] = None
                    selected_piece = None
                    selected_coords = None

                    if player_turn == "w":
                        player_turn = "b"
                    else:
                        player_turn = "w"

                    render_board()  # Re-render the board after the move
                else:
                    # Select a piece to move
                    if row < 8 and column < 8:  # Ensure that the player cannot go out of bounds.
                        selected_piece = chessBoardPositions[row][column]
                    else:
                        selected_piece = None
                        selected_coords = None
                    if selected_piece and selected_piece[0] == player_turn:
                        selected_coords = (row, column)
                    else:
                        selected_piece = None


def valid_moves(piece, chessboard, position):
    piece_type = piece[1]
    moves = []

    if piece_type == "P":  # Movement Rules for Pawn
        moves = pawn_movement(piece, chessboard, position)

    if piece_type == "R":  # Movement rules for Rook
        moves = rook_movement(piece, chessboard, position)

    if piece_type == "B":  # Movement rules for Bishop
        moves = bishop_movement(piece, chessboard, position)

    if piece_type == "Q":  # Movement Rules for Queen
        moves = rook_movement(piece, chessboard, position)
        moves += bishop_movement(piece, chessboard, position)

    if piece_type == "K":
        moves = king_movement(piece, chessboard, position)

    if piece_type == "N":  # Movement rules for Knight
        moves = knight_movement(piece, chessboard, position)

    return moves


def pawn_movement(piece, chessboard, position):
    row, column = position
    piece_color = piece[0]
    moves = []

    if piece_color == "w":
        movement = -1  # Pawns can only move forward so a white pawn would move towards blacks position
        start_row = 6
    else:
        movement = 1
        start_row = 1

    if chessboard[row + movement][column] is None:
        moves.append((row + movement, column))
    if row == start_row and chessboard[row + movement][column] is None and chessboard[row + 2 * movement][column] is None:
        moves.append((row + 2 * movement, column))

    newRow = row + movement
    newColumn = column + movement
    if 0 <= newRow <= 7 and 0 <= newColumn <= 7 and chessboard[newRow][newColumn] is not None:
        if chessboard[newRow][newColumn][0] != piece_color:
            moves.append((newRow, newColumn))
    newColumn = column - movement
    if 0 <= newRow <= 7 and 0 <= newColumn <= 7 and chessboard[newRow][newColumn] is not None:
        if chessboard[newRow][newColumn][0] != piece_color:
            moves.append((newRow, newColumn))
    return moves


def rook_movement(piece, chessboard, position):
    row, column = position
    piece_color = piece[0]
    moves = []
    for newRow in range(8):
        if chessboard[newRow][column] is None:
            moves.append((newRow, column))
        if chessboard[newRow][column] is not None and chessboard[newRow][column][0] != piece_color:
            moves.append((newRow, column))
    for newColumn in range(8):
        if chessboard[row][newColumn] is None:
            moves.append((row, newColumn))
        if chessboard[row][newColumn] is not None and chessboard[row][newColumn][0] != piece_color:
            moves.append((row, newColumn))
    return moves


def bishop_movement(piece, chessboard, position):
    row, column = position
    piece_color = piece[0]
    moves = []
    movement = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Top-left, top-right, bottom-left, bottom-right
    for direction in movement:
        rowDirection, columnDirection = direction
        newRow, newColumn = row, column
        while True:
            newRow += rowDirection
            newColumn += columnDirection
            if 0 <= newRow < 8 and 0 <= newColumn < 8:  # Stay within bounds
                if chessboard[newRow][newColumn] is None:  # Empty square
                    moves.append((newRow, newColumn))
                if chessboard[newRow][newColumn] is not None and chessboard[newRow][newColumn][0] != piece_color:  # Capture opponent piece
                    moves.append((newRow, newColumn))
            else:
                break
    return moves


def king_movement(piece, chessboard, position):
    piece_color = piece[0]
    row, column = position
    moves = []
    movements = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for direction in movements:
        rowDirection, columnDirection = direction
        newRow, newColumn = row + rowDirection, column + columnDirection

        if 0 <= newRow < 8 and 0 <= newColumn < 8:  # Check bounds
            if chessboard[newRow][column] is None:
                moves.append((newRow, column))
            if chessboard[row][newColumn] is None:
                moves.append((row, newColumn))
            if chessboard[newRow][newColumn] is None:
                moves.append((newRow, newColumn))
            if chessboard[newRow][column] is not None and chessboard[newRow][column][0] != piece_color:
                moves.append((newRow, column))
            if chessboard[row][newColumn] is not None and chessboard[row][newColumn][0] != piece_color:
                moves.append((row, newColumn))
            if chessboard[newRow][newColumn] is not None and chessboard[newRow][newColumn][0] != piece_color:
                moves.append((newRow, newColumn))
    return moves


def knight_movement(piece, chessboard, position):
    piece_color = piece[0]
    row, column = position
    movement = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    moves = []
    for direction in movement:
        rowDirection, columnDirection = direction
        newRow, newColumn = row + rowDirection, column + columnDirection
        if 0 <= newRow < 8 and 0 <= newColumn < 8:  # Check bounds
            if chessboard[newRow][newColumn] is None:  # Empty square
                moves.append((newRow, newColumn))
            elif chessboard[newRow][newColumn][0] != piece_color:  # Capture opponent's piece
                moves.append((newRow, newColumn))
    return moves


pygame.quit()
