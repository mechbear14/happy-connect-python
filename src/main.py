import pygame
from collections import namedtuple
import os

from src.Scenes import MainScene

pygame.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Happy Connect")

this_path = os.path.dirname(os.path.realpath(__file__))
filenames = ["icon1.png", "icon2.png", "icon3.png"]
icon_list = [pygame.image.load(os.path.join(this_path, "..", "assets", filename)).convert_alpha()
             for filename in filenames]

Context = namedtuple("Context", ["screen", "icon_list"])
scene = MainScene(Context(screen=screen, icon_list=icon_list))
scene.mainloop()
