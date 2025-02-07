import os
import pygame
import Chessboard

pygame.display.set_caption('Better Chess Analysis')

condition = True

while condition:
    user_input = input("Are you importing a game? (y/n) ").lower()
    if user_input == 'y':
        file_name = input("Enter the game file name (without .txt): ") + ".txt"
        if os.path.isfile(file_name):
            # Read moves & notes from file
            moves, notes = Chessboard.import_game_from_text(file_name)
            # Now pass these moves to the updated generate_board function
            Chessboard.generate_board(imported_game=(moves, notes))
            condition = False
        else:
            print("The file doesn't exist! Please try again.")
    elif user_input == 'n':
        # Start a fresh game
        Chessboard.generate_board()
        condition = False
    else:
        print("Please enter y or n.")
