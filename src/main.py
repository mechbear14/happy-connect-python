import pygame
from collections import namedtuple

from src.Scenes import MainScene

pygame.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Happy Connect")

Context = namedtuple("Context", ["screen"])
scene = MainScene(Context(screen))
scene.mainloop()
