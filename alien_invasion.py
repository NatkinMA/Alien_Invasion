import sys

import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.clock = pygame.time.Clock()                # Объект для отслеживания игрового времени.
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)

    def run_game(self):
        """Запускает основной цикл игры."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            self.clock.tick(60)                         # Устанавливаем частоту кадров игры.

    def _check_events(self):
        """Обработка нажатия клавиш и события мыши."""
        for event in pygame.event.get():                # Отслеживание событий клавиатуры и мыши.
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Обновление изображения на экране и отображение нового экрана."""
        self.screen.fill(self.settings.bg_color)        # При каждом проходе поверхность заливается выбранным цветом.
        self.ship.blitme()
        pygame.display.flip()                           # Отображение последнего прорисованного экрана.


if __name__ == "__main__":
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
