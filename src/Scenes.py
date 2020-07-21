import pygame
from typing import NamedTuple, Tuple
from src.Game import Scene
from src.Core import Board
from src.Sprites import BoardSprite, PathSprite


class MainScene(Scene):
    def __init__(self, context: NamedTuple):
        Scene.__init__(self, context)
        self.rows = 8
        self.columns = 8
        self.kinds_of_blocks = 3

        self.board = Board(self.rows, self.columns, self.kinds_of_blocks)
        self.board_position = pygame.Vector2(0, 100)
        self.board_size = pygame.Vector2(400, 400)
        board_size_int = int(self.board_size.x), int(self.board_size.y)
        board_region = pygame.Surface(board_size_int)
        self.board_sprite = BoardSprite(self.board, board_region, context.icon_list)

        self.selected = []
        self.selecting = False
        self.path_sprite = PathSprite(self.board_position, self.board_size,
                                      self.board_sprite.get_block_size())

    def on_mouse_down(self, button: Tuple, position: Tuple):
        if button[0]:
            block = mouse_row, mouse_col = self.mouse_on_which_block(position)
            if mouse_row > -1 and mouse_col > -1:
                self.selecting = True
                self.selected.append(block)

    def on_mouse_move(self, position: Tuple):
        if self.selecting:
            board = self.board.get_board()
            mouse = mouse_row, mouse_col = self.mouse_on_which_block(position)
            last_row, last_col = self.selected[-1]
            backtrack = len(self.selected) > 1 and mouse == self.selected[-2]
            if backtrack:
                self.selected.pop()
                return
            on_screen = mouse_row > -1 and mouse_col > -1
            is_neighbour = abs(mouse_row - last_row) < 2 and abs(mouse_col - last_col) < 2
            same_colour = board[mouse_row][mouse_col] == board[last_row][last_col]
            not_same = not (mouse_row == last_row and mouse_col == last_col)
            no_cross = self.selected.count((mouse_row, mouse_col)) == 0
            correct = all([on_screen, is_neighbour, same_colour, not_same, no_cross])
            if correct:
                self.selected.append(mouse)

    def on_mouse_up(self, button: Tuple, position: Tuple):
        self.selected = []
        self.selecting = False

    def render(self):
        self.board_sprite.render(self.context.screen, self.board_position, self.selected)
        self.path_sprite.render(self.context.screen, self.selected)

    def on_destroy(self):
        pygame.quit()
        raise SystemExit

    def mouse_on_which_block(self, position: Tuple) -> Tuple:
        block_size = self.board_sprite.get_block_size()
        mouse_position = pygame.Vector2(position)
        offset = mouse_position - self.board_position
        column_index, column_remain = divmod(offset.x, block_size.x)
        row_index, row_remain = divmod(offset.y, block_size.y)
        column_index = column_index if -1 < column_index < self.columns else -1
        row_index = row_index if -1 < row_index < self.rows else -1

        row_col = int(row_index), int(column_index)
        touch_ratio = 0.8
        touch_low, touch_high = 0.5 - touch_ratio / 2, 0.5 + touch_ratio / 2
        column_in_touch = touch_low < column_remain / block_size.x < touch_high
        row_in_touch = touch_low < row_remain / block_size.y < touch_high
        if column_in_touch and row_in_touch:
            return row_col
        else:
            return -1, -1
