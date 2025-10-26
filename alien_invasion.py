import sys

import pygame

from settings import Settings


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

    def run_game(self):
        """Запускает основной цикл игры."""
        while True:
            for event in pygame.event.get():            # Отслеживание событий клавиатуры и мыши.
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(self.settings.bg_color)    # При каждом проходе поверхность заливается выбранным цветом.
            pygame.display.flip()                       # Отображение последнего прорисованного экрана.
            self.clock.tick(60)                         # Устанавливаем частоту кадров игры.


if __name__ == "__main__":
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
