import unittest
import pygame
from collections import namedtuple
import numpy

from src.Core import Board
from src.Scenes import MainScene
from src.Sprites import BoardSprite
from src.Game import Play

pygame.init()

screen = pygame.Surface((400, 600))
board_image = pygame.Surface((400, 400))
assets = dict(icon_list=None, board_image=board_image)
data = {}
Context = namedtuple("Context", ["screen", "assets", "data"])
context = Context(screen=screen, assets=assets, data=data)
board = numpy.array([[0, 0, 0, 0],
                     [1, 1, 2, 1],
                     [2, 2, 2, 2],
                     [3, 3, 2, 3]])
button = (True, False, False)
position = [(i * 100 + 50, j * 100 + 150) for j in range(4) for i in range(4)]
position.extend([(10, 80)])
scene = MainScene(context)


class MainSceneTests(unittest.TestCase):
    def setUp(self) -> None:
        global scene
        scene = MainScene(context)
        scene.board = Board(4, 4, 4)
        scene.board.board = board.copy()
        scene.board_region = pygame.Surface((400, 400))
        scene.board_position = pygame.Vector2(0, 100)
        scene.board_sprite = BoardSprite(scene.board, scene.board_region)

    def test_click_on_block(self):
        self.setUp()
        scene.on_mouse_down(button, position[2])
        self.assertEqual(scene.selected, [(0, 2)])

    def test_click_out_of_screen(self):
        self.setUp()
        scene.on_mouse_down(button, position[16])
        self.assertEqual(scene.selected, [])

    def test_mouse_move_normally_on_blocks(self):
        self.setUp()
        scene.on_mouse_down(button, position[6])
        scene.on_mouse_move(position[9])
        scene.on_mouse_move(position[10])
        scene.on_mouse_move(position[11])
        scene.on_mouse_move(position[14])
        self.assertEqual(scene.selected, [(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)])
        scene.on_mouse_up(button, position[14])
        self.assertEqual(scene.selected, [])

    def test_mouse_move_only_after_mouse_down(self):
        self.setUp()
        scene.on_mouse_move(position[6])
        scene.on_mouse_move(position[9])
        scene.on_mouse_move(position[10])
        scene.on_mouse_move(position[11])
        scene.on_mouse_move(position[14])
        self.assertEqual(scene.selected, [])

    def test_mouse_move_backtrack(self):
        self.setUp()
        scene.on_mouse_down(button, position[11])
        scene.on_mouse_move(position[10])
        scene.on_mouse_move(position[11])
        scene.on_mouse_move(position[6])
        scene.on_mouse_move(position[10])
        self.assertEqual(scene.selected, [(2, 3), (1, 2), (2, 2)])

    def test_mouse_move_on_same_block(self):
        self.setUp()
        scene.on_mouse_down(button, position[0])
        scene.on_mouse_move(position[0])
        self.assertEqual(scene.selected, [(0, 0)])

    def test_mouse_move_out_of_screen(self):
        self.setUp()
        scene.on_mouse_down(button, position[0])
        scene.on_mouse_move(position[1])
        scene.on_mouse_move(position[16])
        scene.on_mouse_move(position[2])
        self.assertEqual(scene.selected, [(0, 0), (0, 1), (0, 2)])

    def test_move_mouse_on_different_colours(self):
        self.setUp()
        scene.on_mouse_down(button, position[0])
        scene.on_mouse_move(position[4])
        scene.on_mouse_move(position[1])
        self.assertEqual(scene.selected, [(0, 0), (0, 1)])

    def test_move_mouse_not_on_neighbours(self):
        self.setUp()
        scene.on_mouse_down(button, position[0])
        scene.on_mouse_move(position[6])
        scene.on_mouse_move(position[1])
        self.assertEqual(scene.selected, [(0, 0), (0, 1)])

    def test_move_mouse_with_circles(self):
        self.setUp()
        scene.on_mouse_down(button, position[8])
        scene.on_mouse_move(position[9])
        scene.on_mouse_move(position[10])
        scene.on_mouse_move(position[11])
        scene.on_mouse_move(position[6])
        scene.on_mouse_move(position[10])
        scene.on_mouse_move(position[14])
        self.assertEqual(scene.selected, [(2, 0), (2, 1), (2, 2), (2, 3), (1, 2)])


end_game = None


class PlayTest(unittest.TestCase):
    @staticmethod
    def on_win(picked_count):
        global end_game
        end_game = picked_count

    @staticmethod
    def on_lose(picked_count):
        global end_game
        end_game = picked_count

    def test_win(self):
        global end_game
        end_game = None
        target = [2, 2, 2, 2, 2, 2]
        play = Play(target, 10, PlayTest.on_win, PlayTest.on_lose)
        for r in range(6):
            won, lost = play.update(r, 3)
            self.assertEqual(play.picked_counts[r], target[r])
            self.assertTrue(not won if r < 5 else won)
            self.assertTrue(not lost)
        self.assertEqual(end_game, target)

    def test_lose(self):
        target = [2, 2, 2, 2, 2, 2]
        play = Play(target, 2, PlayTest.on_win, PlayTest.on_lose)
        play.update(0, 3)
        won, lost = play.update(1, 3)
        self.assertTrue(not won)
        self.assertTrue(lost)
        self.assertEqual(end_game, [2, 2, 0, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()
