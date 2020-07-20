from pygame.sprite import Sprite
from pygame.font import Font
from pygame import Surface, Vector2, Color
from typing import List
from src.Core import Board


class BoardSprite(Sprite):
    def __init__(self, board: Board, surface: Surface, image_list: List[Surface] = None):
        Sprite.__init__(self)
        self.image = surface
        self.rect = surface.get_rect()

        width, height = self.rect.width, self.rect.height
        self.dimension = board.get_board().shape
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
            row, column = divmod(array_index, int(self.dimension[1]))
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

    def render(self, screen: Surface, position: Vector2):
        px = int(position.x)
        py = int(position.y)
        for block in self.blocks:
            block.render(self.image)
        screen.blit(self.image, self.image.get_rect(topleft=(px, py)))


class BlockSprite(Sprite):
    def __init__(self, position: Vector2, image: Surface):
        Sprite.__init__(self)
        px = int(position.x)
        py = int(position.y)
        self.image = image
        self.rect = image.get_rect(topleft=(px, py))

    def render(self, board_surface: Surface):
        board_surface.blit(self.image, self.rect)
