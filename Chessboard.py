import pygame
import ChessPieces


class Chessboard:  # Chessboard is a class that holds all the game state logic, UI logic, and functionality of the main program.
    pass


def generate_board():  # Generates the chessboard and the pieces in starting position.
    pygame.init()  # Initiate pygame function/methods.

    CHESS_ROWS = 8
    CHESS_COLUMNS = 8

    # Loading chess board
    screen = pygame.display.set_mode((512, 800))  # Dimensions of our window.
    # Load in images for the dark/light squares.
    dark_square = pygame.image.load("images/ChessDarkSquare.png").convert()
    light_square = pygame.image.load("images/ChessLightSquare.png").convert()

    chessboard_positions = [  # Chessboard positions is an array that keeps track of the board, a lot of movement operations stem from changing this array.
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]

    piece_image = {  # A dictionary of all the pieces in the chessboard array mapped to the images.
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

    chess_notation = [  # Map of all the squares within the chessboard.
        ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
        ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
        ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
        ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
        ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
        ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
        ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
        ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"],
    ]
    piece_notation = ["R", "N", "B", "Q", "K"]
    chess_notation = ["x", "+", "#", "e.p", "O-O", "O-O-O"]

    def render_ui():  # This function renders the starting position of the chessboard and updates it as the game progresses.
        # x and y coordinate used to track user coordinates (later stored as row and column) and to help generate the squares and pieces on the board.
        x_coordinate = 0
        y_coordinate = 0

        # Draw the chessboard
        for row in range(CHESS_ROWS):
            for column in range(CHESS_COLUMNS):
                square = light_square if (row + column) % 2 == 0 else dark_square
                screen.blit(square, (x_coordinate, y_coordinate))  # Print the colored square on the board based on the previous operation
                x_coordinate += 64  # xCoordinate increased print the square on the next column.
            # This resets and moves on to the next row.
            x_coordinate = 0
            y_coordinate += 64

        # Draw the chess pieces
        for row in range(CHESS_ROWS):
            for column in range(CHESS_COLUMNS):
                piece = chessboard_positions[row][column]  # piece is a variable that takes in a square of chessboard_positions.
                if piece:
                    screen.blit(piece_image[piece], (column * 64 + 6, row * 64 + 6))  # If the square is holding a piece, identify the piece via dictionary and print the image corresponding.

        for king_color in ['w', 'b']:  # This for loop checks if the king is in check and highlights if it is.
            in_check, king_position = is_king_in_check(chessboard_positions, king_color)
            if in_check:
                highlight_square(screen, king_position, (255, 0, 0))  # Red for check/checkmate

        for king_color in ['w', 'b']:  # For if the king is in checkmate.
            if is_checkmate(chessboard_positions, king_color):
                font = pygame.font.SysFont(None, 48)
                if king_color == 'w':
                    text = font.render("Checkmate! White loses.", True, (255, 0, 0))
                else:
                    text = font.render("Checkmate! Black loses.", True, (255, 0, 0))
                screen.blit(text, (10, 700))

        for king_color in ['w', 'b']:  # If the position is a stalemate as a result of the king having no valid movements but not in check.
            if is_checkmate(chessboard_positions, king_color):
                font = pygame.font.SysFont(None, 48)
                text = font.render("It's a stalemate!", True, (255, 0, 0))
        pygame.display.flip()

    render_ui()  # Initial render of the board and pieces

    running = True  # Variable to ensure the window stays up.
    selected_piece = None
    selected_coords = None
    # White always starts first.
    player_turn = "w"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit button stops the game.
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Main event for if player selects a piece.
                # TODO: Specify MOUSEBUTTONDOWN to be Mouse 1.
                xCoordinate, yCoordinate = event.pos
                # Divide by 64 to get good coordinate system (if at (64,64), coord will be (1,1)) FLOOR OPERATION IMPORTANT.
                row = yCoordinate // 64
                column = xCoordinate // 64

                if selected_piece:  # If there is a piece selected, check to see if user clicks on same square.
                    if selected_coords == (row, column):  # This assures that the player will have to reselect.
                        selected_piece = None
                        selected_coords = None

                if selected_piece:  # If player tries to make invalid move, reset coords and selected piece
                    if (row, column) not in valid_moves(selected_piece, chessboard_positions, selected_coords):  # Prevents user from making invalid moves.
                        selected_piece = None
                        selected_coords = None

                if selected_piece:  # Move the piece to the square then update
                    if (row, column) in valid_moves(selected_piece, chessboard_positions, selected_coords):  # Check if the new row, column is a valid move.
                        chessboard_positions[row][column] = selected_piece  # In the array, replace the square selected with the piece selected.
                        chessboard_positions[selected_coords[0]][selected_coords[1]] = None  # Replace the previous coordinates with None
                    # Empty the variables for the next turn.
                    selected_piece = None
                    selected_coords = None

                    # Alternate turns between white and black.
                    player_turn = "b" if player_turn == "w" else "w"

                    render_ui()  # Re-render the board after the move.
                else:  # Selecting a piece.
                    if row < 8 and column < 8:  # Ensure that the player cannot go out of bounds.
                        selected_piece = chessboard_positions[row][column]  # Select a piece from the array.
                    else:  # If player tries to go out of bounds, reset, so they have to choose again.
                        selected_piece = None
                        selected_coords = None
                    if selected_piece and selected_piece[0] == player_turn:  # selected_piece[0] checks to see if the piece color corresponds with the player turn and selected_piece checks to see if a piece exists.
                        selected_coords = (row, column)  # Stores the piece coordinates.
                    else:
                        selected_piece = None


def valid_moves(piece, chessboard, position, check_safety=True):  # valid_moves stores all the moves that a piece can do, movement logic stored in separate variables.
    piece_type = piece[1]
    moves = []  # Array stores the list of (row, column) a piece can move.

    # Movement logic for the different pieces.
    if piece_type == "P":  # Movement Rules for Pawn
        moves = pawn_movement(piece, chessboard, position)

    if piece_type == "R":  # Movement rules for Rook
        moves = rook_movement(piece, chessboard, position)

    if piece_type == "B":  # Movement rules for Bishop
        moves = bishop_movement(piece, chessboard, position)

    if piece_type == "Q":  # Movement rules for Queen
        moves = rook_movement(piece, chessboard, position) + bishop_movement(piece, chessboard, position)

    if piece_type == "K":  # Movement rules for King
        moves = king_movement(piece, chessboard, position)

    if piece_type == "N":  # Movement rules for Knight
        moves = knight_movement(piece, chessboard, position)

    if check_safety:  # If on, it will filter moves that leave the king in check and return moves that will not leave it in check.
        filteredMoves = []
        for move in moves:  # Go through each legal move in moves list to filter any moves that would leave the king in check.
            if not leaves_king_in_check(piece, chessboard, position, move):
                filteredMoves.append(move)  # Append then return the moves that do NOT leave the king in check.
        return filteredMoves

    return moves


def pawn_movement(piece, chessboard, position):  # Main logic for pawn movement.
    row, column = position
    piece_color = piece[0]
    moves = []  # Return to main valid_moves array.

    if piece_color == "w":  # Checks to see color to determine direction of movement and starting row for double pawn movements.
        movement = -1  # Pawns can only move forward so a white pawn would move towards blacks position
        start_row = 6
    else:
        movement = 1
        start_row = 1

    if chessboard[row + movement][column] is None:  # Single pawn movement, checks to see if row above is empty.
        moves.append((row + movement, column))
    if row == start_row and chessboard[row + movement][column] is None and chessboard[row + 2 * movement][column] is None:  # Double pawn movement logic.
        moves.append((row + 2 * movement, column))

    new_row = row + movement
    new_column = column + movement
    if 0 <= new_row <= 7 and 0 <= new_column <= 7 and chessboard[new_row][new_column] is not None:  # Ensures the piece stays in bounds when capturing diagonally and that there is a piece there.
        if chessboard[new_row][new_column][0] != piece_color:  # Checks to see if piece is its own color.
            moves.append((new_row, new_column))  # Add capture to legal move list.
    # Ditto but for the opposite diagonal.
    new_column = column - movement
    if 0 <= new_row <= 7 and 0 <= new_column <= 7 and chessboard[new_row][new_column] is not None:
        if chessboard[new_row][new_column][0] != piece_color:
            moves.append((new_row, new_column))
    return moves


def rook_movement(piece, chessboard, position):  # Movement logic for the rook or just straight lines.
    row, column = position
    piece_color = piece[0]
    moves = []
    movement = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # This array stores all the different directions a piece, the rook, can move.

    for direction in movement:  # for loop goes through each iteration of movement to calculate legal moves.
        rowDirection, columnDirection = direction  # for the offset
        new_row, new_column = row, column  # Start from the current position
        while True:
            new_row += rowDirection
            new_column += columnDirection
            if 0 <= new_row < 8 and 0 <= new_column < 8:  # Stay within bounds
                if chessboard[new_row][new_column] is None:  # Check if empty square.
                    moves.append((new_row, new_column))
                elif chessboard[new_row][new_column][0] != piece_color:  # Capture opponent piece
                    moves.append((new_row, new_column))
                    break  # Stop moving in this direction after capturing
                else:
                    break  # Stop moving in this direction if blocked by own piece
            else:
                break  # Stop if out of bounds
    return moves


def bishop_movement(piece, chessboard, position):  # Movement logic for bishops, diagonals.
    row, column = position
    piece_color = piece[0]
    moves = []
    movement = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # All the different directions a bishop can move.
    for direction in movement:  # Goes through each iteration of movement directions.
        rowDirection, columnDirection = direction  # Offset
        new_row, new_column = row, column
        while True:  # Goes through each diagonal to see which moves are legal.
            new_row += rowDirection
            new_column += columnDirection
            if 0 <= new_row < 8 and 0 <= new_column < 8:  # Stay within bounds
                if chessboard[new_row][new_column] is None:  # Empty square
                    moves.append((new_row, new_column))
                elif chessboard[new_row][new_column] is not None and chessboard[new_row][new_column][0] != piece_color:  # Capture opponent piece
                    moves.append((new_row, new_column))
                    break  # If capture piece, stop calculating moves
                else:
                    break  # If blocked by own piece, stop calculating moves.
            else:
                break  # If out of bounds, stop calculating moves.
    return moves


def king_movement(piece, chessboard, position):  # Movement logic for the king.
    piece_color = piece[0]
    row, column = position
    moves = []
    movements = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # Each direction the king can move.
    for direction in movements:  # Goes through each iteration of movements to see legal moves.
        rowDirection, columnDirection = direction  # for offset
        new_row, new_column = row + rowDirection, column + columnDirection

        if 0 <= new_row < 8 and 0 <= new_column < 8:  # Check bounds
            # Movement logic for all directions.
            if chessboard[new_row][column] is None:
                moves.append((new_row, column))
            if chessboard[row][new_column] is None:
                moves.append((row, new_column))
            if chessboard[new_row][new_column] is None:
                moves.append((new_row, new_column))
            if chessboard[new_row][column] is not None and chessboard[new_row][column][0] != piece_color:
                moves.append((new_row, column))
            if chessboard[row][new_column] is not None and chessboard[row][new_column][0] != piece_color:
                moves.append((row, new_column))
            if chessboard[new_row][new_column] is not None and chessboard[new_row][new_column][0] != piece_color:
                moves.append((new_row, new_column))
    return moves


def knight_movement(piece, chessboard, position):  # Movement logic for the knight.
    piece_color = piece[0]
    row, column = position
    movement = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]  # Each direction a knight can move.
    moves = []
    for direction in movement:  # Goes through each iteration of movements to see legal moves.
        rowDirection, columnDirection = direction
        new_row, new_column = row + rowDirection, column + columnDirection
        if 0 <= new_row < 8 and 0 <= new_column < 8:  # Stay within bounds.
            if chessboard[new_row][new_column] is None:  # Check if square is empty.
                moves.append((new_row, new_column))
            elif chessboard[new_row][new_column][0] != piece_color:  # Capture opponent's piece
                moves.append((new_row, new_column))
    return moves


def is_king_in_check(chessboard, king_color):  # This function returns the position of the king and true/false for if the king is in check.
    # Kind coords.
    king_position = None

    # Determine piece color that can check player on players turn (if white, then black, else white)
    opponent_color = "b" if king_color == "w" else "w"

    # Find the king's position
    for row in range(8):
        for column in range(8):
            piece = chessboard[row][column]
            if piece == king_color + "K":  # Find the king's position
                king_position = (row, column)  # Store kings position
                break
        if king_position:  # If king position is found, break out of for loop.
            break

    # Check if any opponent piece can attack the king
    for row in range(8):
        for column in range(8):
            piece = chessboard[row][column]  # finds piece
            if piece and piece[0] == opponent_color:  # Opponent's piece
                if king_position in valid_moves(piece, chessboard, (row, column), check_safety=False):  # check_safety false means that it in valid_moves, it won't recursively call valid_moves so in this call, that if statement is skipped.
                    return True, king_position  # If in check, return true and the position.

    return False, king_position


def leaves_king_in_check(piece, chessboard, start, end):  # Checks to see if moving a piece will leave it in check.
    piece_color = piece[0]
    simulated_board = simulate_board(chessboard, piece, start, end)  # simulate_board copies the board state and helps simulate position if a piece moves to determine if a king is in check.
    is_in_check, _ = is_king_in_check(simulated_board, piece_color)
    return is_in_check


def simulate_board(chessboard, piece, start, end):  # Simulates the board
    simulated_board = [row[:] for row in chessboard]  # Create a copy of the board
    simulated_board[end[0]][end[1]] = piece  # Place the piece at the new position
    simulated_board[start[0]][start[1]] = None  # Remove the piece from the old position
    return simulated_board


def is_checkmate(chessboard, player_color):  # Checkmate function
    # If the king is not in check, it's not checkmate
    in_check, _ = is_king_in_check(chessboard, player_color)

    if not in_check:
        return False

    # Check if the player has any legal moves left
    for row in range(8):
        for column in range(8):
            piece = chessboard[row][column]
            if piece and piece[0] == player_color:
                valid_moves_list = valid_moves(piece, chessboard, (row, column))  # Check all player piece and see if any of the pieces can legally move.
                if valid_moves_list:  # If any move is possible, return false
                    return False

    return True  # No legal moves and the king is in checkmate.


def is_stalemate(chessboard, player_color):  # Stalemate function
    in_check, _ = is_king_in_check(chessboard, player_color)

    if in_check:  # If the king is in check, it can't be a stalemate.
        return False

    for row in range(8):  # Go through every piece to see if they can move.
        for column in range(8):
            piece = chessboard[row][column]
            if piece and piece[0] == player_color:
                valid_moves_list = valid_moves(piece, chessboard, (row, column))  # Check all player piece and see if any of the pieces can legally move.
                if valid_moves_list:  # If any move is possible, return false
                    return False

    return True  # No legal moves but the king isn't in check.


def highlight_square(screen, position, color):  # Function that allows us to highlight squares, reusable.

    row, column = position
    highlight = pygame.Surface((64, 64))
    highlight.set_alpha(128)  # Transparency
    highlight.fill(color)
    screen.blit(highlight, (column * 64, row * 64))


pygame.quit()  # Quit game when finished running.
