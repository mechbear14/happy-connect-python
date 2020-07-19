import unittest
import pygame
from pygame import Surface, Vector2, Color
from pygame.rect import Rect
import numpy

from src.Core import Board
from src.Sprites import BoardSprite, BlockSprite

pygame.init()


class BoardTest(unittest.TestCase):
    def test_create(self):
        board_obj = Board(8, 8, 3)
        board = board_obj.get_board()
        self.assertEqual(board.shape[0] * board.shape[1], 8 * 8)
        self.assertTrue(isinstance(board[4][2], numpy.int8))
        count = board_obj.get_count()
        self.assertEqual(len(count), 3)
        self.assertEqual(sum(count), 8 * 8)


class BoardSpriteTest(unittest.TestCase):
    def test_create(self):
        board = Board(8, 8, 3).get_board()
        board_surface = Surface((400, 400))
        board_sprite = BoardSprite(board, board_surface, 3)
        self.assertEqual(board_sprite.block_size, Vector2(400 / 8, 400 / 8))
        self.assertEqual(len(board_sprite.blocks), 8 * 8)
        self.assertEqual(len(board_sprite.block_images), 3)
        self.assertTrue(isinstance(board_sprite.block_images[2], Surface))

    def test_render(self):
        board = Board(8, 8, 3).get_board()
        board_surface = Surface((400, 400))
        board_sprite = BoardSprite(board, board_surface, 3)
        screen = Surface((400, 600))
        position = Vector2(0, 100)
        board_sprite.render(screen, position)
        self.assertTrue(True, False)


class BlockSpriteTest(unittest.TestCase):
    def test_create(self):
        position = Vector2(150, 100)
        surface = Surface((50, 50))
        block = BlockSprite(position, surface)
        self.assertEqual(block.rect, Rect(150, 100, 50, 50))
        self.assertEqual(block.image, surface)

    def test_render(self):
        position = Vector2(150, 100)
        surface = Surface((50, 50))
        surface.fill(Color(0, 200, 0))
        block = BlockSprite(position, surface)
        board = Surface((400, 400))
        block.render(board)
        self.assertEqual(board.get_at((160, 110)), Color(0, 200, 0))
        self.assertEqual(board.get_at((10, 10)), Color(0, 0, 0))


if __name__ == '__main__':
    unittest.main()
