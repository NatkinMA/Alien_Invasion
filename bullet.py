import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управления снарядами, выпущенными кораблем."""

    def __init__(self, ai_game):
        """Создаем объект снаряда в текущей позиции корабля."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Снаряд создается в позиции (0, 0) и назначается правильная позиция.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Сохраняем позицию снаряда в вещественном формате.
        self.y = float(self.rect.y)

    def update(self):
        """Перемещение снаряда вверх по экрану."""
        # Обновление точной позиции снаряда.
        self.y -= self.settings.bullet_speed
        # Обновляем позицию прямоугольника.
        self.rect.y = self.y

    def draw_bullet(self):
        """Рисуем снаряд на экране."""
        pygame.draw.rect(self.screen, self.color, self.rect)
