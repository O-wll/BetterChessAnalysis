import Chessboard
import ChessPieces
import pygame

running = True

pygame.display.set_caption('Better Chess Analysis')

Chessboard.generate_board()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
