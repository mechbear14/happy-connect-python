import pygame
import os

from src.Game import Context, Play, Scene
from src.Scenes import MainScene, TitleScene, WinScene, LoseScene

pygame.init()

screen = pygame.display.set_mode((400, 650))
pygame.display.set_caption("Happy Connect")

this_path = os.path.dirname(os.path.realpath(__file__))
filenames = ["icon1.png", "icon2.png", "icon3.png", "icon4.png", "icon5.png", "icon6.png"]
icon_list = [pygame.image.load(os.path.join(this_path, "..", "assets", filename)).convert_alpha()
             for filename in filenames]
board_image = pygame.image.load(os.path.join(this_path, "..", "assets", "board.png"))
play_image = pygame.image.load(os.path.join(this_path, "..", "assets", "play.png"))

scenes = []


def add_scene(next_scene: Scene):
    scenes.append(next_scene)


target = [10, 10, 10, 10, 10, 10]


def on_win(*args):
    scenes.append(WinScene(context))
    pygame.event.post(pygame.event.Event(pygame.QUIT, {}))


def on_lose(*args):
    scenes.append(LoseScene(context))
    pygame.event.post(pygame.event.Event(pygame.QUIT, {}))


play = Play(target, 40, on_win, on_lose)
assets = dict(icon_list=icon_list, board_image=board_image, play_image=play_image)
data = dict(play=play, scenes=scenes)
context = Context(screen, assets, data)

add_scene(TitleScene(context))

while len(scenes) > 0:
    scene = scenes.pop()
    scene.mainloop()

pygame.quit()
raise SystemExit
