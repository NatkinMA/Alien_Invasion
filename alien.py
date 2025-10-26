import pygame

from pygame.sprite import Sprite

class Alien(Sprite):
    """Класс, описывающий пришельца."""

    def __init__(self, ai_game):
        """Инициализируем пришельца и задаем его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen

        # Загрузка изображения пришельца и назначение атрибута rect.
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Пришелец появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохраняем горизонтальную позицию пришельца.
        self.x = float(self.rect.x)
