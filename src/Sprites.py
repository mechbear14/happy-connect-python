import numpy
import pygame
from pygame.sprite import Sprite
from pygame.font import Font
from pygame import Surface, Vector2, Color
from pygame.locals import *
from pygame.draw import circle, aalines
from typing import List, Tuple
from src.Core import Board
from src.Game import Animation, Timeline, ANIMATION_BEGIN, Play


class BoardSprite(Sprite):
    def __init__(self, board: Board, surface: Surface, image_list: List[Surface] = None):
        Sprite.__init__(self)
        self.image = surface
        self.rect = surface.get_rect()
        self.board = board

        width, height = self.rect.width, self.rect.height
        self.board_row_count, self.board_column_count = board.get_board().shape
        self.block_size = Vector2()
        self.block_size.x = width / board.get_board().shape[0]
        self.block_size.y = height / board.get_board().shape[1]

        if image_list is None:
            block_images = [self.get_default_image(number) for number in range(board.block_kind_count)]
        else:
            block_images = image_list.copy()
            if len(block_images) < board.block_kind_count:
                more_images = [self.get_default_image(number)
                               for number in range(len(image_list), board.block_kind_count)]
                block_images.extend(more_images)
        self.block_images = block_images

        self.new_blocks = []
        self.blocks = []
        self.sync_board()

        self.timeline = Timeline(0)

    def sync_board(self):
        self.new_blocks = [None] * (self.board_row_count * self.board_column_count)
        self.blocks = []
        for array_index, block_kind in enumerate(self.board.get_board().flat):
            row, column = divmod(array_index, int(self.board_column_count))
            screen_position = Vector2()
            screen_position.x = column * self.block_size.x
            screen_position.y = row * self.block_size.y
            self.blocks.append(BlockSprite(screen_position, self.block_images[block_kind]))

    def get_default_image(self, number: int) -> Surface:
        sw, sh = int(self.block_size.x), int(self.block_size.y)
        surface = Surface((sw, sh))
        font = Font(None, 24)
        image = font.render(f"{number}", True, Color(255, 255, 255))
        cx, cy = int(sw / 2), int(sh / 2)
        surface.blit(image, image.get_rect(center=(cx, cy)))
        return surface

    def get_block_size(self) -> Vector2:
        return self.block_size

    def board_to_sprite_index(self, board_index: Tuple) -> int:
        row, column = board_index
        return column + self.board_row_count * row

    def get_position_by_index(self, board_index: Tuple) -> Vector2:
        row, column = board_index
        return Vector2(column, row).elementwise() * self.block_size

    def add_animation(self, animations: List[Tuple]):
        to_hide = []
        to_slide = []
        for a in animations:
            if a[2] == -1 and a[3] == -1:
                to_hide.append(a)
            else:
                to_slide.append(a)
                if a[0] < 0 or a[1] < 0:
                    temp_index = self.board_to_sprite_index((a[0], a[1]))
                    position = self.get_position_by_index((a[0], a[1]))
                    new_board = self.board.get_board()
                    image = self.block_images[new_board[a[2], a[3]]]
                    self.new_blocks[temp_index] = BlockSprite(position, image)
        for index, a in enumerate(to_hide):
            block_index = self.board_to_sprite_index((a[0], a[1]))
            block = self.blocks[block_index]
            animation = Animation(begin_state=None,
                                  end_state=None,
                                  delay=self.timeline.get_last_time(),
                                  duration=100,
                                  setter=block.hide)
            self.timeline.add_animation(animation)

        common_delay = self.timeline.get_last_time()
        for index, a in enumerate(to_slide):
            block_index = self.board_to_sprite_index((a[0], a[1]))
            block = self.new_blocks[block_index] if block_index < 0 else self.blocks[block_index]
            animation = Animation(begin_state=self.get_position_by_index((a[0], a[1])),
                                  end_state=self.get_position_by_index((a[2], a[3])),
                                  delay=common_delay,
                                  duration=500,
                                  setter=block.slide)
            self.timeline.add_animation(animation)

    def play_animation(self, begin_tick: int):
        self.timeline.animation_begin(begin_tick)
        event = pygame.event.Event(ANIMATION_BEGIN, dict(timeline_id=0))
        pygame.event.post(event)

    def on_animation_end(self):
        self.sync_board()
        self.timeline.reset_clock()

    def update(self, ticks: int):
        self.timeline.update(ticks)

    def render(self, screen: Surface, position: Vector2, selected: List[Tuple]):
        px = int(position.x)
        py = int(position.y)
        pixels = self.image.copy()
        for index, block in enumerate(self.blocks):
            row, column = divmod(index, int(self.board_column_count))
            block_selected = selected.count((row, column)) > 0
            block.render(pixels, block_selected)
        for index, block in enumerate(self.new_blocks):
            if block is not None:
                block.render(pixels, False)
        screen.blit(pixels, pixels.get_rect(topleft=(px, py)))


class BlockSprite(Sprite):
    def __init__(self, position: Vector2, image: Surface):
        Sprite.__init__(self)
        px, py = int(position.x), int(position.y)
        self.image = image
        self.base_rect = image.get_rect(topleft=(px, py))
        self.rect = image.get_rect(topleft=(px, py))
        self.show = True

    def get_base_rect(self) -> Tuple:
        return self.base_rect

    def slide(self, begin_state: Vector2, end_state: Vector2, progress: float):
        # mapped_progress = 0.5 + (progress - 0.25) * (progress - 0.5) * (progress - 0.75) / (0.75 * 0.25)
        mapped_progress = progress
        target = begin_state.lerp(end_state, mapped_progress)
        base_x, base_y = self.base_rect.topleft
        dx, dy = int(target.x) - base_x, int(target.y) - base_y
        self.rect = self.base_rect.move(dx, dy)

    def hide(self, *args):
        self.show = False

    def render(self, board_surface: Surface, selected: bool = False):
        if self.show:
            board_surface.blit(self.image, self.rect)
            if selected:
                cover = Surface((self.image.get_size()))
                cover.fill(Color(100, 100, 100))
                board_surface.blit(cover, self.rect, special_flags=BLEND_MULT)


class PathSprite(Sprite):
    def __init__(self, board_position: Vector2, board_size: Vector2, block_size: Vector2):
        Sprite.__init__(self)
        board_position_int = int(board_position.x), int(board_position.y)
        board_size_int = int(board_size.x), int(board_size.y)
        self.block_width, self.block_height = int(block_size.x), int(block_size.y)
        self.image = Surface(board_size_int)
        self.image.fill(Color(0, 0, 0))
        self.rect = Rect(board_position_int, board_size_int)

    def render(self, screen: Surface, selected: List[Tuple]):
        if len(selected) > 0:
            circle_centres = [((col + 0.5) * self.block_width, (row + 0.5) * self.block_height)
                              for (row, col) in selected]
            surface = self.image.copy()
            if len(selected) > 1:
                aalines(surface, Color(255, 255, 255), False, circle_centres)
            for centre in circle_centres:
                circle(surface, Color(255, 255, 255), centre, 5)
            screen.blit(surface, self.rect, special_flags=BLEND_MAX)


class PlaySprite(Sprite):
    def __init__(self, play: Play, play_image: Surface, play_position: Vector2):
        Sprite.__init__(self)
        self.timeline = Timeline(1)
        self.play_position = play_position
        self.play = play
        self.target = self.play.target.copy()
        self.picked_count = self.play.picked_counts.copy()
        self.updating_kind = None
        self.centre_rights = [(140, 25), (240, 25), (340, 25), (140, 75), (240, 75), (340, 75)]
        self.top_lefts = [(50, 0), (150, 0), (250, 0), (50, 50), (150, 50), (250, 50)]
        self.image = play_image

        px, py = int(play_position.x), int(play_position.y)
        self.rect = self.image.get_rect(topleft=(px, py))

    def add_animation(self, update_kind: int, update_count: int):
        self.updating_kind = update_kind
        begin_state = self.picked_count[update_kind]
        end_state = begin_state + update_count
        animation = Animation(begin_state=begin_state,
                              end_state=end_state,
                              delay=self.timeline.get_last_time(),
                              duration=update_count * 100,
                              setter=self.set_text)
        self.timeline.add_animation(animation)

    def play_animation(self, begin_tick: int):
        self.timeline.animation_begin(begin_tick)
        event = pygame.event.Event(ANIMATION_BEGIN, dict(timeline_id=1))
        pygame.event.post(event)

    def on_animation_end(self):
        self.updating_kind = None
        self.sync_play()
        self.timeline.reset_clock()

    def sync_play(self):
        self.target = self.play.target.copy()
        self.picked_count = self.play.picked_counts.copy()

    def set_text(self, begin_state: int, end_state: int, progress: float):
        current_count = begin_state + int(numpy.floor(progress * (end_state - begin_state)))
        current_count = min(current_count, self.target[self.updating_kind])
        self.picked_count[self.updating_kind] = current_count

    def update(self, ticks: int):
        self.timeline.update(ticks)

    def render(self, screen: Surface, icon_list: List[Surface]):
        pixels = self.image.copy()
        font = Font(None, 24)
        for i, _ in enumerate(self.target):
            current = self.picked_count[i]
            target = self.target[i]
            topleft = self.top_lefts[i]
            centre_right = self.centre_rights[i]
            block_image = icon_list[i]
            pixels.blit(block_image, block_image.get_rect(topleft=topleft))
            font_surface = font.render(f"{current} / {target}", True, Color(255, 255, 255))
            pixels.blit(font_surface, font_surface.get_rect(midright=centre_right))
        screen.blit(pixels, self.rect)
