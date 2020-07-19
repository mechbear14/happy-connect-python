import pygame
from pygame.locals import *

from src.Core import Board
from src.Sprites import BoardSprite

pygame.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Happy Connect")
board_region = pygame.Surface((400, 400))
board = Board(8, 8, 3).get_board()
board_position = pygame.Vector2(0, 100)
board_image = BoardSprite(board, board_region, 3)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit
    board_image.render(screen, board_position)
    pygame.display.update()
