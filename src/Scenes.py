import pygame
import os
from typing import NamedTuple
from src.Game import Scene
from src.Core import Board
from src.Sprites import BoardSprite


class MainScene(Scene):
    def __init__(self, context: NamedTuple):
        Scene.__init__(self, context)
        this_path = os.path.dirname(os.path.realpath(__file__))
        icon1 = pygame.image.load(os.path.join(this_path, "..", "assets", "icon1.png")).convert_alpha()
        icon2 = pygame.image.load(os.path.join(this_path, "..", "assets", "icon2.png")).convert_alpha()
        icon3 = pygame.image.load(os.path.join(this_path, "..", "assets", "icon3.png")).convert_alpha()
        board = Board(8, 8, 3).get_board()
        board_region = pygame.Surface((400, 400))
        self.board_position = pygame.Vector2(0, 100)
        self.board_sprite = BoardSprite(board, board_region, 3, [icon1, icon2, icon3])

    def render(self):
        self.board_sprite.render(self.context.screen, self.board_position)

    def on_destroy(self):
        pygame.quit()
        raise SystemExit
