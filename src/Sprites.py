import numpy
import pygame
from pygame.sprite import Sprite
from pygame.font import Font
from pygame import Surface, Vector2, Color
from pygame.locals import *
from pygame.draw import circle, aalines
from typing import List, Tuple
from src.Core import Board
from src.Game import Animation, Timeline, ANIMATION_BEGIN


class BoardSprite(Sprite):
    # Change this to accepting numpy board and block kind count
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

        self.timeline = Timeline()

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

    def setup_animation(self, animations: List[Tuple], new_board: numpy.ndarray, begin_tick: int):
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
                    image = self.block_images[new_board[a[2], a[3]]]
                    self.new_blocks[temp_index] = BlockSprite(position, image)
        for index, a in enumerate(to_hide):
            block_index = self.board_to_sprite_index((a[0], a[1]))
            block = self.blocks[block_index]
            animation = Animation(begin_state=None,
                                  end_state=None,
                                  delay=index * 100,
                                  duration=100,
                                  setter=block.hide)
            self.timeline.add_animation(animation)
        for index, a in enumerate(to_slide):
            block_index = self.board_to_sprite_index((a[0], a[1]))
            block = self.new_blocks[block_index] if block_index < 0 else self.blocks[block_index]
            animation = Animation(begin_state=self.get_position_by_index((a[0], a[1])),
                                  end_state=self.get_position_by_index((a[2], a[3])),
                                  delay=len(to_hide) * 100,
                                  duration=500,
                                  setter=block.slide)
            self.timeline.add_animation(animation)

        self.timeline.animation_begin(begin_tick)
        event = pygame.event.Event(ANIMATION_BEGIN, {})
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
        target = begin_state.lerp(end_state, progress)
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
                cover.fill(Color(128, 128, 128))
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
