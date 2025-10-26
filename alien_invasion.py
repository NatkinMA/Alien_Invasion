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
            self._update_screen()
            self.clock.tick(60)                         # Устанавливаем частоту кадров игры.

    def _check_events(self):
        """Обработка нажатия клавиш и события мыши."""
        for event in pygame.event.get():  # Отслеживание событий клавиатуры и мыши.
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        """Обновление изображения на экране и отображение нового экрана."""
        self.screen.fill(self.settings.bg_color)  # При каждом проходе поверхность заливается выбранным цветом.
        self.ship.blitme()
        pygame.display.flip()  # Отображение последнего прорисованного экрана.


if __name__ == "__main__":
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
