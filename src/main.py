import pygame
from pygame.locals import *
import os

from src.Core import Board
from src.Sprites import BoardSprite

pygame.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Happy Connect")
board_region = pygame.Surface((400, 400))
board = Board(8, 8, 3).get_board()
board_position = pygame.Vector2(0, 100)

this_path = os.path.dirname(os.path.realpath(__file__))
icon1 = pygame.image.load(os.path.join(this_path, "..", "assets", "icon1.png")).convert_alpha()
icon2 = pygame.image.load(os.path.join(this_path, "..", "assets", "icon2.png")).convert_alpha()
icon3 = pygame.image.load(os.path.join(this_path, "..", "assets", "icon3.png")).convert_alpha()
board_image = BoardSprite(board, board_region, 3, [icon1, icon2, icon3])

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit
    board_image.render(screen, board_position)
    pygame.display.update()
