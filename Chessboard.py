import pygame
import ChessPieces
from collections import defaultdict


class Chessboard:  # Chessboard is a class that holds all the game state logic, UI logic, and functionality of the main program.
    pass


# This variable is used throughout multiple functions including generate_board, so it has to be a global variable. for accessibility.
castling_rights = {
    "wK": True,  # White can still castle king side
    "wQ": True,  # White can still castle queen side
    "bK": True,  # Black can still castle king side
    "bQ": True  # Black can still castle queen side
}


def copy_board(board):  # This function is a helper function that takes in the chessboard, copies it, and returns it.
    return [row[:] for row in board]


def export_game_to_txt(chess_notation, notes_by_move, filename):  # This function runs when the user exits the program, it will create a file with the users moves and notes so that they are saved.
    with open(filename, 'w', encoding='utf-8') as f:
        for move_line in chess_notation:  # First, take the moves list stored in chess_notation and write to external file.
            f.write(move_line + '\n')
        f.write("---NOTES---\n")
        for move_number, note_text in notes_by_move.items():  # Then, write the notes sections IF applicable.
            if note_text.strip():
                f.write(f"{move_number}. {note_text}\n")


def import_game_from_text(filename):  # This function allows users to import their games and will adjust the starting variables storing notes and moves to the values returned by this function.

    # The two variables most important, chess_notation which stores the move lists, and notes_by_move, which stores the list of notes the user makes.
    chess_notation = []
    notes_by_move = defaultdict(str)  # Ordinary dictionary of strings. Useful for more dynamic operations.

    with open(filename, 'r', encoding='utf-8') as f:  # Removes new line from file when storing values into
        lines = [line.strip('\n') for line in f]

    if "---NOTES---" in lines:  # If this line is detected in notes, moves will be recorded and THEN the notes.
        notes_start_index = lines.index("---NOTES---")  #
        move_lines = lines[:notes_start_index]
        note_lines = lines[notes_start_index + 1:]
        # 1) Parse moves
        for line in move_lines:
            line = line.strip()
            if line:
                chess_notation.append(line)
        # 2) Parse notes
        for line in note_lines:
            line = line.strip()
            if line:
                parts = line.split('.', 1)
                if len(parts) == 2:
                    move_num_str, note_text = parts
                    move_num_str = move_num_str.strip()
                    note_text = note_text.strip()
                    try:
                        move_num = int(move_num_str)
                        notes_by_move[move_num] = note_text
                    except ValueError:
                        print("Error Detected")
    else:
        # No '------NOTES----' found, so treat ALL lines as moves
        for line in lines:
            line = line.strip()
            if line:
                chess_notation.append(line)
    return chess_notation, notes_by_move


def generate_board(imported_game=None):  # The main function where the board is generated and encapsulates all the game rules and game flow.
    pygame.init()

    CHESS_ROWS = 8
    CHESS_COLUMNS = 8
    player_turn = "w"
    screen = pygame.display.set_mode((1100, 800))
    pygame.display.set_caption("Chess")

    NOTES_AREA_LEFT = 550
    NOTES_AREA_TOP = 20
    NOTES_AREA_WIDTH = 400
    NOTES_AREA_HEIGHT = 400
    notes_rect = pygame.Rect(NOTES_AREA_LEFT, NOTES_AREA_TOP, NOTES_AREA_WIDTH, NOTES_AREA_HEIGHT)

    # Load square images
    dark_square = pygame.image.load("images/ChessDarkSquare.png").convert()
    light_square = pygame.image.load("images/ChessLightSquare.png").convert()

    # Default board
    default_board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]

    # If we're given imported_game as (chess_notation, notes_by_move), apply it
    if imported_game:
        # imported_game should be a tuple: (chess_notation, notes_by_move)
        loaded_notation, loaded_notes = imported_game

        # Apply moves
        chessboard, chessboard_positions, notes_by_move = apply_imported_game(
            loaded_notation,
            notes_by_move=loaded_notes
        )

        # The final position after all moves
        _, latest_player_turn = chessboard_positions[-1]
        player_turn = latest_player_turn

        # Save the moves (for display in the UI)
        chess_notation = [line.strip() for line in loaded_notation if line.strip()]

        # Count how many moves we have
        move_count = sum(1 for ln in chess_notation if '.' in ln)

    else:
        # No imported game
        chessboard = copy_board(default_board)
        chessboard_positions = [(copy_board(chessboard), "w")]
        chess_notation = []
        move_count = 0
        notes_by_move = defaultdict(str)

    # Piece images
    piece_image = {
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

    square_list = [
        ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
        ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
        ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
        ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
        ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
        ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
        ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
        ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"],
    ]

    running = True
    selected_piece = None
    selected_coords = None
    current_position_index = len(chessboard_positions) - 1
    last_move = None
    is_typing_note = False

    def get_full_move_index(pos_index):  # Gets the index of what move number it is.
        return (pos_index + 1) // 2

    def coords_to_square(row, col):  # Converts coordinates (E4) to the actual square (4, 4)
        return square_list[row][col]

    def build_move_notation(chessboard, piece, start, end, capture=False, castling=False):  # Function that determines what move was made and returns the appropriate notation. Checks/Checkmates are handled
        if castling:  # If castling is true, determined which castle.
            start_col = start[1]
            end_col = end[1]
            if end_col == start_col + 2:  # King side castling
                return "O-O"
            else:  # Queen side castling
                return "O-O-O"

        piece_type = piece[1]
        start_square = coords_to_square(start[0], start[1])
        end_square = coords_to_square(end[0], end[1])
        if piece_type == 'P':  # In case pawn moves or captures.
            if capture:
                return f"{start_square[0]}x{end_square}"
            else:
                return end_square
        else:
            piece_symbol_map = {
                'N': 'N',
                'B': 'B',
                'R': 'R',
                'Q': 'Q',
                'K': 'K',
            }
            symbol = piece_symbol_map.get(piece_type, '?')  # Determines what piece symbol to grab from dictionary.
            if capture:  # If capture,
                return f"{symbol}x{end_square}"
            else:
                return f"{symbol}{end_square}"

    def render_ui():  # The actual UI of the chessboard, move notation, notes, everything.
        screen.fill((173, 216, 230))
        x_coordinate = 0
        y_coordinate = 0

        # Draw squares
        for row in range(CHESS_ROWS):
            for column in range(CHESS_COLUMNS):
                square = light_square if (row + column) % 2 == 0 else dark_square
                screen.blit(square, (x_coordinate, y_coordinate))
                x_coordinate += 64
            x_coordinate = 0
            y_coordinate += 64

        # Draw pieces
        for row in range(CHESS_ROWS):
            for column in range(CHESS_COLUMNS):
                piece = chessboard[row][column]
                if piece:
                    screen.blit(piece_image[piece], (column * 64 + 6, row * 64 + 6))

        # Highlight kings in check
        for king_color in ['w', 'b']:
            in_check, king_position = is_king_in_check(chessboard, king_color)
            if in_check and king_position:
                highlight_square(screen, king_position, (255, 0, 0))

        # Checkmate / Stalemate messages
        for king_color in ['w', 'b']:
            if is_checkmate(chessboard, king_color):
                font_cm = pygame.font.SysFont(None, 48)
                text = font_cm.render(f"Checkmate! {'White' if king_color == 'w' else 'Black'} loses.", True, (255, 0, 0))
                screen.blit(text, (50, 250))
            elif is_stalemate(chessboard, king_color):
                font_sm = pygame.font.SysFont(None, 48)
                text = font_sm.render("It's a stalemate!", True, (255, 0, 0))
                screen.blit(text, (50, 250))

        # Display player turn
        font_turn = pygame.font.SysFont(None, 36)
        turn_text = "White's Move" if player_turn == "w" else "Black's Move"
        turn_surface = font_turn.render(turn_text, True, (0, 0, 0))
        pygame.draw.rect(screen, (173, 216, 230), pygame.Rect(10, 520, 200, 40))
        screen.blit(turn_surface, (10, 525))

        # Variables for displaying the chess notation.
        font_notation = pygame.font.SysFont(None, 28)
        max_lines_per_column = 12
        line_height = 20
        start_x = 10
        start_y = 550
        column_spacing = 150
        current_x = start_x
        current_y = start_y

        for i, line in enumerate(chess_notation):  # Display chess notation on the screen.
            if i % max_lines_per_column == 0 and i != 0:  # If maximum lines has been reached, make a new column.
                current_x += column_spacing
                current_y = start_y
            move_text = font_notation.render(line, True, (0, 0, 0))
            screen.blit(move_text, (current_x, current_y))
            current_y += line_height

        # White rectangle for notes area
        pygame.draw.rect(screen, (255, 255, 255), notes_rect)
        pygame.draw.rect(screen, (0, 0, 0), notes_rect, 2)

        # Draw current note text
        current_note = notes_by_move[get_full_move_index(current_position_index)]
        font_notes = pygame.font.SysFont(None, 24)
        note_lines = current_note.split('\n')
        text_y = NOTES_AREA_TOP + 5
        for line in note_lines:
            text_surface = font_notes.render(line, True, (0, 0, 0))
            screen.blit(text_surface, (NOTES_AREA_LEFT + 5, text_y))
            text_y += 25

        pygame.display.flip()

    render_ui()  # Run first instance of rendering ui

    while running:  # Main logic when running game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Export on quit if desired
                export_game_to_txt(chess_notation, notes_by_move, "ChessGame.txt")
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if notes_rect.collidepoint(event.pos):  # Check if user is trying to make notes.
                    is_typing_note = not is_typing_note
                    render_ui()
                    continue

                xCoordinate, yCoordinate = event.pos
                row = yCoordinate // 64
                column = xCoordinate // 64

                if selected_piece and selected_coords == (row, column):  # If user clicks on the same square, let them reselect piece.
                    selected_piece = None
                    selected_coords = None

                if selected_piece:
                    possible_moves = valid_moves(selected_piece, chessboard, selected_coords, last_move=last_move)  # Get the list of valid moves for selected piece.
                    if (row, column) not in possible_moves:  # Cancel their selection if user picks square that is not possible.
                        selected_piece = None
                        selected_coords = None
                    else:
                        capture = False
                        if chessboard[row][column] is not None:  # If capture is possible, enable capture flag for notation.
                            capture = True
                        # In case move is enpassant.
                        if selected_piece[1] == 'P' and column != selected_coords[1] and chessboard[row][column] is None:
                            capture = True
                            capture_row = row + 1 if selected_piece[0] == 'w' else row - 1
                            chessboard[capture_row][column] = None

                        # Update chessboard to reflect making move.
                        chessboard[row][column] = selected_piece
                        chessboard[selected_coords[0]][selected_coords[1]] = None

                        # Castling
                        castling = False
                        if selected_piece[1] == "K" and abs(column - selected_coords[1]) == 2:
                            castling = True
                            if column == selected_coords[1] + 2:
                                chessboard[row][5] = chessboard[row][7]
                                chessboard[row][7] = None
                            else:
                                chessboard[row][3] = chessboard[row][0]
                                chessboard[row][0] = None

                        # Update castling rights
                        if selected_piece[1] == "K":
                            if selected_piece[0] == "w":
                                castling_rights["wK"] = False
                                castling_rights["wQ"] = False
                            else:
                                castling_rights["bK"] = False
                                castling_rights["bQ"] = False
                        if selected_piece[1] == "R":
                            if selected_piece[0] == "w" and selected_coords[0] == 7:
                                if selected_coords[1] == 0:
                                    castling_rights["wQ"] = False
                                elif selected_coords[1] == 7:
                                    castling_rights["wK"] = False
                            if selected_piece[0] == "b" and selected_coords[0] == 0:
                                if selected_coords[1] == 0:
                                    castling_rights["bQ"] = False
                                elif selected_coords[1] == 7:
                                    castling_rights["bK"] = False

                        double_pawn = (selected_piece[1] == 'P' and abs(row - selected_coords[0]) == 2)  # Boolean to determine if pawn if moved, was a double pawn move.

                        # Last move is a dictionary that keeps track of the last move made, primarily used for en passant logic.
                        last_move = {
                            "piece": selected_piece,
                            "start": selected_coords,
                            "end": (row, column),
                            "double_pawn_move": double_pawn
                        }

                        # Promotion
                        promotion_symbol = ""
                        if selected_piece[1] == 'P':  # Check to make sure the piece is a pawn.
                            if (selected_piece[0] == 'w' and row == 0) or (selected_piece[0] == 'b' and row == 7):
                                promoted_piece = selected_piece[0] + 'Q'  # Auto promote pawn to a Queen.
                                chessboard[row][column] = promoted_piece
                                promotion_symbol = "=Q"  # Symbol used when making the chess notation.

                        move_notation = build_move_notation(  # For printing move notation to screen
                            chessboard,
                            selected_piece,
                            selected_coords,
                            (row, column),
                            capture=capture,
                            castling=castling
                        )

                        if promotion_symbol:  # If promotion happened, add the symbol on to the current move notation.
                            move_notation += promotion_symbol

                        # Check to see if the move left the opponents king in check to add a check (+) or a checkmate (#) on the notation.
                        opponent_color = "b" if player_turn == "w" else "w"
                        in_check, _ = is_king_in_check(chessboard, opponent_color)
                        if in_check:
                            if is_checkmate(chessboard, opponent_color):
                                move_notation += "#"
                            else:
                                move_notation += "+"

                        if player_turn == "w":  # Appending the move notation to the chess notation
                            move_count += 1
                            notation_entry = f"{move_count}. {move_notation}"
                            chess_notation.append(notation_entry)
                        else:  # If black, print on same line.
                            chess_notation[-1] += f" {move_notation}"

                        player_turn = "b" if player_turn == "w" else "w"  # Switch player turn

                        # Add new chessboard position to the current chessboard_positions array.
                        current_position_index += 1
                        chessboard_positions = chessboard_positions[:current_position_index]
                        chessboard_positions.append((copy_board(chessboard), player_turn))

                        # Deselect player turn and update the ui
                        selected_piece = None
                        selected_coords = None
                        render_ui()
                else:  # Allow player to select a piece on the board.
                    if row < 8 and column < 8:  # Ensure piece selection is inbounds
                        selected_piece = chessboard[row][column]
                        if selected_piece and selected_piece[0] == player_turn:
                            selected_coords = (row, column)
                        else:  # Deselect if invalid.
                            selected_piece = None
                            selected_coords = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # If left arrow key is pressed, go back to the previous position.
                    if current_position_index > 0:
                        current_position_index -= 1
                        temp_board, temp_turn = chessboard_positions[current_position_index]
                        chessboard = copy_board(temp_board)
                        player_turn = temp_turn
                        render_ui()
                elif event.key == pygame.K_RIGHT:  # If right arrow key is pressed, go forward to the next move made.
                    if current_position_index < len(chessboard_positions) - 1:
                        current_position_index += 1
                        temp_board, temp_turn = chessboard_positions[current_position_index]
                        chessboard = copy_board(temp_board)
                        player_turn = temp_turn
                        render_ui()
                elif is_typing_note:  # Handling if notes are being typed.
                    move_idx = get_full_move_index(current_position_index)
                    if event.key == pygame.K_BACKSPACE:  # If user is deleting characters
                        if notes_by_move[move_idx]:
                            notes_by_move[move_idx] = notes_by_move[move_idx][:-1]
                        render_ui()
                    elif event.key == pygame.K_RETURN:  # If user is going to a new line.
                        notes_by_move[move_idx] += '\n'
                        render_ui()
                    else:  # Append user character at the end of current one.
                        notes_by_move[move_idx] += event.unicode
                        render_ui()


def valid_moves(piece, chessboard, position, last_move=None, check_safety=True):  # This function handles the validity of moves pieces can make and filter to ensure valid moves.

    # NOTE: check_safety is for the fact valid_moves is a function that is called from another function (leaves_king_in_check), avoid infinite recursion case.
    piece_type = piece[1]
    if piece_type == "P":
        moves = pawn_movement(piece, chessboard, position, last_move=last_move)
    elif piece_type == "R":
        moves = rook_movement(piece, chessboard, position)
    elif piece_type == "B":
        moves = bishop_movement(piece, chessboard, position)
    elif piece_type == "Q":
        moves = rook_movement(piece, chessboard, position) + bishop_movement(piece, chessboard, position)
    elif piece_type == "K":
        # Pass check_safety to decide castling or not
        moves = king_movement(piece, chessboard, position, can_castle=check_safety)
    elif piece_type == "N":
        moves = knight_movement(piece, chessboard, position)
    else:
        moves = []

    # If we're not enforcing king-safety, just return the moves
    if not check_safety:
        return moves

    # Otherwise, filter out moves that would leave your own king in check
    filtered = []
    for mv in moves:
        if not leaves_king_in_check(piece, chessboard, position, mv):
            filtered.append(mv)
    return filtered


def pawn_movement(piece, chessboard, position, last_move=None):  # Pawn movement function
    row, column = position
    piece_color = piece[0]
    moves = []

    if piece_color == "w":  # Movement depends on pawn color.
        movement = -1
        start_row = 6
    else:
        movement = 1
        start_row = 1

    # Single step
    if 0 <= row + movement < 8:
        if chessboard[row + movement][column] is None:
            moves.append((row + movement, column))

    # Double step
    if row == start_row:
        if (chessboard[row + movement][column] is None and
                chessboard[row + 2 * movement][column] is None):
            moves.append((row + 2 * movement, column))

    # Diagonal captures
    for dc in [-1, 1]:
        new_row = row + movement
        new_column = column + dc
        if 0 <= new_row < 8 and 0 <= new_column < 8:
            if chessboard[new_row][new_column] is not None:
                if chessboard[new_row][new_column][0] != piece_color:
                    moves.append((new_row, new_column))

    # En Passant
    if last_move and last_move["double_pawn_move"]:
        opponent_piece = last_move["piece"]
        if opponent_piece[1] == 'P' and opponent_piece[0] != piece_color:
            opp_end_row, opp_end_col = last_move["end"]
            if opp_end_row == row and abs(opp_end_col - column) == 1:
                en_passant_row = row + movement
                en_passant_col = opp_end_col
                if 0 <= en_passant_row < 8 and 0 <= en_passant_col < 8:
                    if chessboard[en_passant_row][en_passant_col] is None:
                        moves.append((en_passant_row, en_passant_col))
    return moves


def rook_movement(piece, chessboard, position):  # Rook movement function (straight lines)

    row, column = position
    piece_color = piece[0]
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # What directions a pawn can move in.

    for dr, dc in directions:  # For loop to determine legal movements in each direction.
        while True:
            new_row, new_col = row + dr, column + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if chessboard[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif chessboard[new_row][new_col][0] != piece_color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
            else:
                break
    return moves


def bishop_movement(piece, chessboard, position):  # Bishop movement function (diagonals)
    row, column = position
    piece_color = piece[0]
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:  # For loop to determine legal movements in each direction.
        while True:
            new_row, new_col = row + dr, column + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if chessboard[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif chessboard[new_row][new_col][0] != piece_color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
            else:
                break
    return moves


def is_square_attacked(chessboard, square, attacking_color):  # Function that sees if a square is attacked. Useful for determining legal King movements.
    row, col = square
    for r in range(8):
        for c in range(8):
            piece = chessboard[r][c]
            if piece and piece[0] == attacking_color:  # Check to see if the pieces valid moves matches with the square the piece (king) wants to move to.
                if (row, col) in valid_moves(piece, chessboard, (r, c), check_safety=False):  # Ensure no recursion calling!
                    return True
    return False


def king_movement(piece, chessboard, position, can_castle=True):  # King movement function
    piece_color = piece[0]
    row, column = position
    moves = []
    # Directions king can move
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions: 
        new_row, new_col = row + dr, column + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if chessboard[new_row][new_col] is None:
                moves.append((new_row, new_col))
            elif chessboard[new_row][new_col][0] != piece_color:
                moves.append((new_row, new_col))

    # If we're not allowed to handle castling (e.g., check_safety=False), safety precaution against recursion
    if not can_castle:
        return moves

    if piece_color == "w" and (row, column) == (7, 4):  # Castling for the white king
        if castling_rights["wK"]:  # King side castling
            # check squares e1->g1
            if (chessboard[7][5] is None and
                    chessboard[7][6] is None and
                    not is_square_attacked(chessboard, (7, 4), 'b') and
                    not is_square_attacked(chessboard, (7, 5), 'b') and
                    not is_square_attacked(chessboard, (7, 6), 'b')):
                moves.append((7, 6))
        if castling_rights["wQ"]:  # Queen side castling
            # check squares e1->c1
            if (chessboard[7][3] is None and
                    chessboard[7][2] is None and
                    chessboard[7][1] is None and
                    not is_square_attacked(chessboard, (7, 4), 'b') and
                    not is_square_attacked(chessboard, (7, 3), 'b') and
                    not is_square_attacked(chessboard, (7, 2), 'b')):
                moves.append((7, 2))
    elif piece_color == "b" and (row, column) == (0, 4):  # Castling for the black queen.
        if castling_rights["bK"]:  # Castling for the blacks king side.
            if (chessboard[0][5] is None and
                    chessboard[0][6] is None and
                    not is_square_attacked(chessboard, (0, 4), 'w') and
                    not is_square_attacked(chessboard, (0, 5), 'w') and
                    not is_square_attacked(chessboard, (0, 6), 'w')):
                moves.append((0, 6))
        if castling_rights["bQ"]:  # Castling for blacks queen side.
            if (chessboard[0][3] is None and
                    chessboard[0][2] is None and
                    chessboard[0][1] is None and
                    not is_square_attacked(chessboard, (0, 4), 'w') and
                    not is_square_attacked(chessboard, (0, 3), 'w') and
                    not is_square_attacked(chessboard, (0, 2), 'w')):
                moves.append((0, 2))

    return moves


def knight_movement(piece, chessboard, position):  # Knight movement function
    piece_color = piece[0]
    row, column = position
    moves = []
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    for dr, dc in directions:  # Determine legal moves the knight can make.
        new_row, new_col = row + dr, column + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if chessboard[new_row][new_col] is None:
                moves.append((new_row, new_col))
            elif chessboard[new_row][new_col][0] != piece_color:
                moves.append((new_row, new_col))
    return moves


def is_king_in_check(chessboard, king_color):  # This function checks to see if the king is in check, and returns True or False and the kings position.
    king_position = None
    opponent_color = "b" if king_color == "w" else "w"

    for row in range(8):  # Scans the whole board until king position is found.
        for column in range(8):
            piece = chessboard[row][column]
            if piece == king_color + "K":
                king_position = (row, column)
                break
        if king_position:
            break

    for row in range(8):  # Scans the whole board and checks every piece to see if any pieces legal moves attacks the square the king is on.
        for column in range(8):
            piece = chessboard[row][column]
            if piece and piece[0] == opponent_color:
                if king_position in valid_moves(piece, chessboard, (row, column), check_safety=False):
                    return True, king_position
    return False, king_position


def leaves_king_in_check(piece, chessboard, start, end):  # This function simulates the board and then sees if king moves to a square, will it be in check, needed for filtering moves to ensure only legal king moves are made.
    piece_color = piece[0]
    simulated_board = simulate_board(chessboard, piece, start, end)
    is_in_check, _ = is_king_in_check(simulated_board, piece_color)
    return is_in_check


def simulate_board(chessboard, piece, start, end):  # Simulates the entire board by seeing what the board would look like if a move, in usage case the king, what squares would a piece end up in.
    simulated_board = [row.copy() for row in chessboard]
    simulated_board[end[0]][end[1]] = piece
    simulated_board[start[0]][start[1]] = None
    return simulated_board


def is_checkmate(chessboard, player_color):  # Function that determines if king is in checkmate.
    in_check, _ = is_king_in_check(chessboard, player_color)
    if not in_check:  # If not in check, return false.
        return False

    for row in range(8):  # Scans entire board for if player can make valid move while in check.
        for column in range(8):
            piece = chessboard[row][column]
            if piece and piece[0] == player_color:
                if valid_moves(piece, chessboard, (row, column)):  # If valid move found, return false.
                    return False
    return True


def is_stalemate(chessboard, player_color):  # This function determines stalemate.
    in_check, _ = is_king_in_check(chessboard, player_color)
    if in_check:  # If the king is in check, return false.
        return False

    for row in range(8):  # Scans entire board to see if player can make any legal moves.
        for column in range(8):
            piece = chessboard[row][column]
            if piece and piece[0] == player_color:
                if valid_moves(piece, chessboard, (row, column)):
                    return False
    return True


def highlight_square(screen, position, color):  # Function used for highlighting squares.
    row, column = position
    highlight = pygame.Surface((64, 64))
    highlight.set_alpha(128)
    highlight.fill(color)
    screen.blit(highlight, (column * 64, row * 64))


def apply_imported_game(chess_notation, notes_by_move=None):  # This function is for games that are imported and gives functionality like a normal chess game.
    if notes_by_move is None:  # Check to see if there are notes.
        notes_by_move = defaultdict(str)

    # Chessboard
    chessboard = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]
    player_turn = "w"
    move_count = 0
    last_move = None

    # Local castling rights
    local_castling_rights = {
        "wK": True,
        "wQ": True,
        "bK": True,
        "bQ": True
    }

    # Keep track of intermediate positions
    chessboard_positions = [(copy_board(chessboard), player_turn)]

    def algebraic_to_coords(sq):  # Turn chess notation into actual square coordinates/
        file = sq[0].lower()
        rank = sq[1]
        col = ord(file) - ord('a')
        row = 8 - int(rank)
        return row, col

    def update_local_castling_rights(moved_piece, start_pos):  # Function that updates castling rights of the imported game.
        color = moved_piece[0]
        r, c = start_pos
        if moved_piece[1] == "K":
            if color == "w":
                local_castling_rights["wK"] = False
                local_castling_rights["wQ"] = False
            else:
                local_castling_rights["bK"] = False
                local_castling_rights["bQ"] = False
        if moved_piece[1] == "R":
            if color == "w" and r == 7 and c == 0:
                local_castling_rights["wQ"] = False
            elif color == "w" and r == 7 and c == 7:
                local_castling_rights["wK"] = False
            elif color == "b" and r == 0 and c == 0:
                local_castling_rights["bQ"] = False
            elif color == "b" and r == 0 and c == 7:
                local_castling_rights["bK"] = False

    def do_castle(kingside=True):  # Simulating castling in imported game.
        nonlocal chessboard, player_turn, last_move, local_castling_rights
        if player_turn == 'w':  # Handle castling for white
            row = 7
            if kingside:  # Kingside castling for white.
                chessboard[row][4] = None
                chessboard[row][6] = 'wK'
                chessboard[row][7] = None
                chessboard[row][5] = 'wR'
                local_castling_rights["wK"] = False
                local_castling_rights["wQ"] = False
                last_move = {
                    "piece": "wK",
                    "start": (7, 4),
                    "end": (7, 6),
                    "double_pawn_move": False
                }
            else:  # Queenside castling for black.
                chessboard[row][4] = None
                chessboard[row][2] = 'wK'
                chessboard[row][0] = None
                chessboard[row][3] = 'wR'
                local_castling_rights["wK"] = False
                local_castling_rights["wQ"] = False
                last_move = {
                    "piece": "wK",
                    "start": (7, 4),
                    "end": (7, 2),
                    "double_pawn_move": False
                }
        else:  # Handle castling for black.
            row = 0
            if kingside:  # Handle black kingside castling.
                chessboard[row][4] = None
                chessboard[row][6] = 'bK'
                chessboard[row][7] = None
                chessboard[row][5] = 'bR'
                local_castling_rights["bK"] = False
                local_castling_rights["bQ"] = False
                last_move = {
                    "piece": "bK",
                    "start": (0, 4),
                    "end": (0, 6),
                    "double_pawn_move": False
                }
            else:  # Handle black queenside castling.
                chessboard[row][4] = None
                chessboard[row][2] = 'bK'
                chessboard[row][0] = None
                chessboard[row][3] = 'bR'
                local_castling_rights["bK"] = False
                local_castling_rights["bQ"] = False
                last_move = {
                    "piece": "bK",
                    "start": (0, 4),
                    "end": (0, 2),
                    "double_pawn_move": False
                }

    def apply_single_move(move_str):  # Apply single moves, function named this way to allow players to go forward and backward between white and blacks moves.
        nonlocal chessboard, player_turn, last_move, local_castling_rights
        move_str = move_str.strip()
        if not move_str:
            return
        move_str = move_str.replace('+', '').replace('#', '')

        # Castling
        if move_str in ["O-O", "0-0"]:
            do_castle(kingside=True)
            return
        if move_str in ["O-O-O", "0-0-0"]:
            do_castle(kingside=False)
            return

        # Detect promotion
        promotion_piece = None
        if '=' in move_str:
            parts = move_str.split('=')
            promotion_piece = parts[-1]  # 'Q','N','R','B'
            move_str = parts[0]  # e.g. "exd8"

        is_capture = 'x' in move_str

        # Identify piece symbol if present
        piece_symbol = ''
        if len(move_str) > 0 and move_str[0] in ['K', 'Q', 'R', 'B', 'N']:
            piece_symbol = move_str[0]
            move_str = move_str[1:]

        subpart = move_str.split('x')
        dest_part = subpart[-1]  # after 'x' -> e.g. "d5"

        dest_row, dest_col = algebraic_to_coords(dest_part)

        # Find the piece that can legally move.
        piece_found = False
        for r in range(8):
            for c in range(8):
                piece = chessboard[r][c]
                if piece and piece[0] == player_turn:
                    if piece_symbol == '':
                        if piece[1] != 'P':
                            continue
                    else:
                        if piece[1] != piece_symbol:
                            continue

                    candidate_moves = valid_moves(piece, chessboard, (r, c), last_move=last_move)
                    if (dest_row, dest_col) in candidate_moves:
                        # En-passant
                        if piece[1] == 'P' and is_capture and chessboard[dest_row][dest_col] is None:
                            if player_turn == 'w':
                                chessboard[dest_row + 1][dest_col] = None
                            else:
                                chessboard[dest_row - 1][dest_col] = None

                        # Move piece
                        chessboard[r][c] = None
                        chessboard[dest_row][dest_col] = piece

                        # Promotion
                        if promotion_piece and piece[1] == 'P':
                            chessboard[dest_row][dest_col] = player_turn + promotion_piece

                        # last_move
                        double_pawn = (piece[1] == 'P' and abs(dest_row - r) == 2)
                        last_move = {
                            "piece": piece,
                            "start": (r, c),
                            "end": (dest_row, dest_col),
                            "double_pawn_move": double_pawn
                        }

                        # Update castling rights
                        update_local_castling_rights(piece, (r, c))
                        piece_found = True
                        break
            if piece_found:
                break

    # --- Parse each line in `chess_notation` and apply moves ---
    for line in chess_notation:
        line = line.strip()
        if not line:
            continue

        tokens = line.split()
        filtered_tokens = [t for t in tokens if not t.endswith('.')]

        for half_move in filtered_tokens:
            apply_single_move(half_move)
            # Store board state
            chessboard_positions.append((copy_board(chessboard), player_turn))
            # Switch turns
            player_turn = 'b' if player_turn == 'w' else 'w'
        move_count += 1

    # Return the final board, the positions, and the notes that we were passed.
    return chessboard, chessboard_positions, notes_by_move


pygame.quit()
