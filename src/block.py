import pygame
from pygame.locals import *
import loader

class Block(pygame.sprite.Sprite):
    def __init__(self, screen_rect_left, screen_rect_top, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = loader.load_image("brick.png")
        # ブロックの位置を更新
        self.rect.left = screen_rect_left + x * self.rect.width
        self.rect.top = screen_rect_top + y * self.rect.height
