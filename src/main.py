import pygame
from collections import namedtuple
import os

from src.Game import Play
from src.Scenes import MainScene

pygame.init()

screen = pygame.display.set_mode((400, 650))
pygame.display.set_caption("Happy Connect")

this_path = os.path.dirname(os.path.realpath(__file__))
filenames = ["icon1.png", "icon2.png", "icon3.png", "icon4.png", "icon5.png", "icon6.png"]
icon_list = [pygame.image.load(os.path.join(this_path, "..", "assets", filename)).convert_alpha()
             for filename in filenames]
board_image = pygame.image.load(os.path.join(this_path, "..", "assets", "board.png"))

target = [10, 10, 10, 10, 10, 10]


def on_win(*args):
    print("You win")


def on_lose(*args):
    print("You lose")


play = Play(target, 40, on_win, on_lose)
play_image = pygame.image.load(os.path.join(this_path, "..", "assets", "play.png"))

Context = namedtuple("Context", ["screen", "icon_list", "board_image", "play", "play_image"])
scene = MainScene(Context(screen=screen, icon_list=icon_list, board_image=board_image,
                          play=play, play_image=play_image))
scene.mainloop()
