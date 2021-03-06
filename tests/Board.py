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
        self.assertTrue(isinstance(board[4, 2], numpy.int8))
        count = board_obj.get_count()
        self.assertEqual(len(count), 3)
        self.assertEqual(sum(count), 8 * 8)

    def test_update(self):
        board_obj = Board(4, 4, 4)
        board_obj.board = numpy.array([[0, 0, 0, 0],
                                       [1, 1, 2, 1],
                                       [2, 2, 2, 2],
                                       [3, 3, 2, 3]])
        to_remove = [(2, 0), (2, 1), (1, 2), (2, 2), (3, 2), (2, 3)]
        diff = board_obj.update(to_remove)
        test_indices = [(1, 0), (1, 1), (1, 3), (2, 0), (2, 1), (2, 3), (3, 0),
                        (3, 1), (3, 2), (3, 3)]
        expected = [0, 0, 0, 1, 1, 1, 3, 3, 0, 3]
        for i, e in zip(test_indices, expected):
            self.assertEqual(board_obj.board[i[0], i[1]], e)
        value, count = numpy.unique(board_obj.board, return_counts=True)
        count_dict = dict(zip(value, count))
        self.assertRaises(KeyError, lambda: count_dict[-1])
        self.assertTrue(-1 < numpy.amax(board_obj.board) < 4)

        expected_animations = [(2, 0, -1, -1), (2, 1, -1, -1), (1, 2, -1, -1), (2, 2, -1, -1),
                               (3, 2, -1, -1), (2, 3, -1, -1), (1, 0, 2, 0), (0, 0, 1, 0),
                               (-1, 0, 0, 0), (1, 1, 2, 1), (0, 1, 1, 1), (-1, 1, 0, 1),
                               (0, 2, 3, 2), (-1, 2, 2, 2), (-2, 2, 1, 2), (-3, 2, 0, 2),
                               (1, 3, 2, 3), (0, 3, 1, 3), (-1, 3, 0, 3)]
        self.assertCountEqual(diff, expected_animations)

    def test_update_2(self):
        board_obj = Board(4, 4, 3)
        board_obj.board = numpy.array([[0, 1, 1, 1],
                                       [1, 1, 2, 1],
                                       [2, 2, 1, 2],
                                       [2, 1, 2, 2]])
        to_remove = [(1, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 2), (3, 1)]
        diff = board_obj.update(to_remove)
        test_indices = [(1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0),
                        (3, 1), (3, 2), (3, 3)]
        expected = [0, 2, 1, 2, 2, 2, 2, 2, 2]
        for i, e in zip(test_indices, expected):
            self.assertEqual(board_obj.board[i[0], i[1]], e)
        value, count = numpy.unique(board_obj.board, return_counts=True)
        count_dict = dict(zip(value, count))
        self.assertRaises(KeyError, lambda: count_dict[-1])
        self.assertTrue(-1 < numpy.amax(board_obj.board) < 3)

        expected_animations = [(1, 0, -1, -1), (0, 1, -1, -1), (0, 2, -1, -1), (0, 3, -1, -1),
                               (1, 3, -1, -1), (2, 2, -1, -1), (3, 1, -1, -1), (0, 0, 1, 0),
                               (1, 1, 2, 1), (2, 1, 3, 1), (1, 2, 2, 2), (-1, 0, 0, 0),
                               (-1, 1, 1, 1), (-2, 1, 0, 1), (-1, 2, 1, 2), (-2, 2, 0, 2),
                               (-1, 3, 1, 3), (-2, 3, 0, 3)]
        self.assertCountEqual(diff, expected_animations)

    def test_update_3(self):
        board_obj = Board(4, 4, 4)
        board_obj.board = numpy.array([[0, 0, 0, 0],
                                       [1, 1, 2, 1],
                                       [2, 2, 2, 2],
                                       [3, 3, 2, 3]])
        to_remove = [(2, 0), (2, 1), (1, 2), (2, 2), (3, 2), (2, 3)]
        to_remove.reverse()
        diff = board_obj.update(to_remove)
        test_indices = [(1, 0), (1, 1), (1, 3), (2, 0), (2, 1), (2, 3), (3, 0),
                        (3, 1), (3, 2), (3, 3)]
        expected = [0, 0, 0, 1, 1, 1, 3, 3, 0, 3]
        for i, e in zip(test_indices, expected):
            self.assertEqual(board_obj.board[i[0], i[1]], e)
        value, count = numpy.unique(board_obj.board, return_counts=True)
        count_dict = dict(zip(value, count))
        self.assertRaises(KeyError, lambda: count_dict[-1])
        self.assertTrue(-1 < numpy.amax(board_obj.board) < 4)

        expected_animations = [(2, 0, -1, -1), (2, 1, -1, -1), (1, 2, -1, -1), (2, 2, -1, -1),
                               (3, 2, -1, -1), (2, 3, -1, -1), (1, 0, 2, 0), (0, 0, 1, 0),
                               (-1, 0, 0, 0), (1, 1, 2, 1), (0, 1, 1, 1), (-1, 1, 0, 1),
                               (0, 2, 3, 2), (-1, 2, 2, 2), (-2, 2, 1, 2), (-3, 2, 0, 2),
                               (1, 3, 2, 3), (0, 3, 1, 3), (-1, 3, 0, 3)]
        self.assertCountEqual(diff, expected_animations)

    def test_check_if_possible_1(self):
        board = Board(4, 4, 3)
        board.board = numpy.array([[1, 0, 0, 1],
                                   [0, 2, 2, 0],
                                   [0, 1, 0, 1],
                                   [2, 0, 2, 2]])
        self.assertTrue(board.is_possible_to_move())

    def test_check_if_possible_2(self):
        board = Board(4, 4, 3)
        board.board = numpy.array([[0, 0, 1, 0],
                                   [0, 1, 2, 2],
                                   [2, 1, 0, 1],
                                   [2, 0, 2, 1]])
        self.assertTrue(board.is_possible_to_move())

    def test_check_if_possible_3(self):
        board = Board(4, 4, 3)
        board.board = numpy.array([[0, 1, 0, 0],
                                   [0, 2, 2, 1],
                                   [1, 1, 0, 1],
                                   [2, 0, 2, 2]])
        self.assertTrue(not board.is_possible_to_move())

    def test_shuffle(self):
        board = Board(4, 4, 3)
        board.board = numpy.array([[0, 1, 0, 0],
                                   [0, 2, 2, 1],
                                   [1, 1, 0, 1],
                                   [2, 0, 2, 2]])
        prev_count = [6, 5, 5]
        board.count = prev_count.copy()
        board.shuffle()
        new_count = board.count
        self.assertTrue(board.is_possible_to_move())
        self.assertEqual(prev_count, new_count)


class BoardSpriteTest(unittest.TestCase):
    def test_create(self):
        board = Board(8, 8, 3)
        board_surface = Surface((400, 400))
        board_sprite = BoardSprite(board, board_surface)
        self.assertEqual(board_sprite.block_size, Vector2(400 / 8, 400 / 8))
        self.assertEqual(len(board_sprite.blocks), 8 * 8)
        self.assertEqual(len(board_sprite.block_images), 3)
        self.assertTrue(isinstance(board_sprite.block_images[2], Surface))

    def test_render(self):
        board = Board(8, 8, 2)
        board.board = numpy.zeros([8, 8], numpy.int8)
        board.board[4][2] = 1
        board_surface = Surface((400, 400))
        image_list = [Surface((50, 50)), Surface((50, 50))]
        image_list[0].fill(Color(200, 0, 0))
        image_list[1].fill(Color(0, 200, 0))
        board_sprite = BoardSprite(board, board_surface, image_list)
        screen = Surface((400, 600))
        position = Vector2(0, 100)
        board_sprite.render(screen, position, [])
        self.assertEqual(screen.get_at((125, 325)), Color(0, 200, 0))
        self.assertEqual(screen.get_at((225, 225)), Color(200, 0, 0))


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
