from pygame.sprite import Sprite
from pygame.font import Font
from pygame import Surface, Vector2, Color
from pygame.locals import *
from pygame.draw import circle, aalines
from typing import List, Tuple
from src.Core import Board


class BoardSprite(Sprite):
    def __init__(self, board: Board, surface: Surface, image_list: List[Surface] = None):
        Sprite.__init__(self)
        self.image = surface
        self.rect = surface.get_rect()

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

        self.blocks = []
        for array_index, block_kind in enumerate(board.get_board().flat):
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

    def render(self, screen: Surface, position: Vector2, selected: List[Tuple]):
        px = int(position.x)
        py = int(position.y)
        for index, block in enumerate(self.blocks):
            row, column = divmod(index, int(self.board_column_count))
            block_selected = selected.count((row, column)) > 0
            block.render(self.image, block_selected)
        screen.blit(self.image, self.image.get_rect(topleft=(px, py)))


class BlockSprite(Sprite):
    def __init__(self, position: Vector2, image: Surface):
        Sprite.__init__(self)
        px, py = int(position.x), int(position.y)
        self.image = image
        self.rect = image.get_rect(topleft=(px, py))

    def render(self, board_surface: Surface, selected: bool = False):
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
