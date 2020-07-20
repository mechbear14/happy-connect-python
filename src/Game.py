import pygame
from pygame.locals import *
from typing import NamedTuple, Tuple


class Scene:
    def __init__(self, context: NamedTuple):
        self.running = True
        self.context = context

    def on_destroy(self):
        pass

    def on_mouse_down(self, button: Tuple, position: Tuple):
        pass

    def on_mouse_move(self, position: Tuple):
        pass

    def on_mouse_up(self, button: Tuple, position: Tuple):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed()
                    position = pygame.mouse.get_pos()
                    self.on_mouse_down(buttons, position)
                elif event.type == MOUSEMOTION:
                    position = pygame.mouse.get_pos()
                    self.on_mouse_move(position)
                elif event.type == MOUSEBUTTONUP:
                    buttons = pygame.mouse.get_pressed()
                    position = pygame.mouse.get_pos()
                    self.on_mouse_up(buttons, position)
            self.update()
            self.render()
            pygame.display.update()
        self.on_destroy()
