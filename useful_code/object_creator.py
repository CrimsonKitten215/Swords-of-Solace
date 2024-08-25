import pygame
import sys

class ObjectCreator:
    """
    A class for creating objects
    """
    def __init__(self, asset: str, x: int, y: int, size: int):
        """
        :param asset: Surface the object will use as a texture
        :param x: X coordinate of object
        :param y: Y coordinate of object
        :param size: The amount the size of the object will be multiplied by
        """
        self.asset = asset
        self.x = x
        self.y = y
        self.width = asset.get_width() * size
        self.height = asset.get_height() * size
        self.draw()

    def draw(self):
        """
        Draws the object
        """
        import main
        main.screen.blit(pygame.transform.scale(self.asset, (self.width * main.screen_size, self.height * main.screen_size)), (self.x * main.screen_size, self.y * main.screen_size, (self.x * main.screen_size) + (self.width * main.screen_size), (self.y * main.screen_size) + (self.height * main.screen_size)))
