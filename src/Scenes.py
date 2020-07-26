import pygame
from pygame import Color
from pygame.font import Font
from pygame.rect import Rect
from typing import Tuple

from src.Game import Scene, Context
from src.Core import Board
from src.Sprites import BoardSprite, PathSprite, PlaySprite


class MainScene(Scene):
    def __init__(self, context: Context):
        Scene.__init__(self, context)
        self.rows = 8
        self.columns = 8
        self.kinds_of_blocks = 6

        self.board = Board(self.rows, self.columns, self.kinds_of_blocks)
        self.board_position = pygame.Vector2(0, 200)
        self.board_size = pygame.Vector2(400, 400)
        board_size_int = int(self.board_size.x), int(self.board_size.y)
        board_region = pygame.Surface(board_size_int)
        board_region.blit(self.context.assets["board_image"], (0, 0, 400, 400))
        self.board_sprite = BoardSprite(self.board, board_region, context.assets["icon_list"])

        self.selected = []
        self.selecting = False
        self.path_sprite = PathSprite(self.board_position, self.board_size,
                                      self.board_sprite.get_block_size())

        play_position = pygame.Vector2(0, 50)
        self.play = self.context.data["play"]
        self.play_sprite = PlaySprite(context.data["play"], context.assets["play_image"], play_position)
        self.animation_playing = [False, False]

    def on_create(self, context: Context):
        pass

    def on_mouse_down(self, button: Tuple, position: Tuple):
        if not any(self.animation_playing):
            if button[0]:
                block = mouse_row, mouse_col = self.mouse_on_which_block(position)
                if mouse_row > -1 and mouse_col > -1:
                    self.selecting = True
                    self.selected.append(block)

    def on_mouse_move(self, position: Tuple):
        if not any(self.animation_playing):
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
        if not any(self.animation_playing):
            if len(self.selected) > 2:
                board = self.board.get_board()
                row, col = self.selected[0]
                update_kind = board[row, col]
                update_count = len(self.selected)
                self.play.update(update_kind, update_count)
                diff = self.board.update(self.selected)

                self.board_sprite.add_animation(diff)
                self.board_sprite.play_animation(pygame.time.get_ticks())
                self.play_sprite.add_animation(update_kind, update_count)
                self.play_sprite.play_animation(pygame.time.get_ticks())
            self.selected = []
            self.selecting = False

    def on_animation_begin(self, timeline_id: int):
        self.animation_playing[timeline_id] = True

    def on_animation_end(self, timeline_id: int):
        self.animation_playing[timeline_id] = False
        if timeline_id == 0:
            self.board_sprite.on_animation_end()
        elif timeline_id == 1:
            self.play_sprite.on_animation_end()

        if not any(self.animation_playing):
            if not self.board.is_possible_to_move():
                diff = self.board.shuffle()
                self.board_sprite.add_animation(diff)
                self.board_sprite.play_animation(pygame.time.get_ticks())

    def update(self, ticks: int):
        if self.animation_playing[0]:
            self.board_sprite.update(ticks)
        if self.animation_playing[1]:
            self.play_sprite.update(ticks)

    def render(self):
        self.board_sprite.render(self.context.screen, self.board_position, self.selected)
        self.path_sprite.render(self.context.screen, self.selected)
        self.play_sprite.render(self.context.screen, self.board_sprite.block_images)

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


class TitleScene(Scene):
    def __init__(self, context: Context):
        Scene.__init__(self, context)
        board_position = (0, 125)
        title_position = (200, 250)
        title = "Happy Connect"
        button_position = (200, 400)
        button_text = "Start"

        self.background = self.context.assets["board_image"]
        self.background_rect = self.background.get_rect(topleft=board_position)
        font = Font(None, 48)
        self.title = font.render(title, True, Color(255, 255, 255))
        self.title_rect = self.title.get_rect(center=title_position)
        self.button = font.render(button_text, True, Color(255, 255, 255))
        self.button_rect = self.button.get_rect(center=button_position)

    def on_mouse_down(self, button: Tuple, position: Tuple):
        if button[0] and self.button_rect.collidepoint(*position):
            scenes = self.context.data["scenes"]
            scenes.append(MainScene(self.context))
            pygame.event.post(pygame.event.Event(pygame.QUIT, {}))

    def render(self):
        screen = self.context.screen
        screen.fill(Color(0, 0, 0))
        screen.blit(self.background, self.background_rect)
        screen.blit(self.title, self.title_rect)
        screen.blit(self.button, self.button_rect)


class WinScene(Scene):
    def __init__(self, context: Context):
        Scene.__init__(self, context)
        board_position = (0, 125)
        title_position = (200, 250)
        title = "You achieved your target"
        button_position = (200, 400)
        button_text = "Back"

        self.background = self.context.assets["board_image"]
        self.background_rect = self.background.get_rect(topleft=board_position)
        font = Font(None, 48)
        self.title = font.render(title, True, Color(255, 255, 255))
        self.title_rect = self.title.get_rect(center=title_position)
        self.button = font.render(button_text, True, Color(255, 255, 255))
        self.button_rect = self.button.get_rect(center=button_position)

    def on_mouse_down(self, button: Tuple, position: Tuple):
        if button[0] and self.button_rect.collidepoint(*position):
            scenes = self.context.data["scenes"]
            scenes.append(TitleScene(self.context))
            pygame.event.post(pygame.event.Event(pygame.QUIT, {}))

    def render(self):
        screen = self.context.screen
        screen.fill(Color(0, 0, 0))
        screen.blit(self.background, self.background_rect)
        screen.blit(self.title, self.title_rect)
        screen.blit(self.button, self.button_rect)


class LoseScene(Scene):
    def __init__(self, context: Context):
        Scene.__init__(self, context)
        board_position = (0, 125)
        title_position = (200, 250)
        title = "You didn't achieve your target"
        button_position = (200, 400)
        button_text = "Start again"

        self.background = self.context.assets["board_image"]
        self.background_rect = self.background.get_rect(topleft=board_position)
        font = Font(None, 48)
        self.title = font.render(title, True, Color(255, 255, 255))
        self.title_rect = self.title.get_rect(center=title_position)
        self.button = font.render(button_text, True, Color(255, 255, 255))
        self.button_rect = self.button.get_rect(center=button_position)

    def on_mouse_down(self, button: Tuple, position: Tuple):
        if button[0] and self.button_rect.collidepoint(*position):
            scenes = self.context.data["scenes"]
            scenes.append(MainScene(self.context))
            pygame.event.post(pygame.event.Event(pygame.QUIT, {}))

    def render(self):
        screen = self.context.screen
        screen.fill(Color(0, 0, 0))
        screen.blit(self.background, self.background_rect)
        screen.blit(self.title, self.title_rect)
        screen.blit(self.button, self.button_rect)
