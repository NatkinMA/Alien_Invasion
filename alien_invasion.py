import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.clock = pygame.time.Clock()                # Объект для отслеживания игрового времени.
        self.settings = Settings()
        """
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        """
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Запускает основной цикл игры."""
        while True:
            self._check_events()
            self.ship.update()
#            self.bullets.update()
            self._update_bullets()
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
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создаем новый снаряд и добавляем его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляем позиции снарядов и удаляем снаряды, достигшие верхней границы экрана."""
        # Обновление позиций снарядов.
        self.bullets.update()
        # Удаляем снаряды, вышедшие за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
#        print(len(self.bullets))


    def _update_screen(self):
        """Обновление изображения на экране и отображение нового экрана."""
        self.screen.fill(self.settings.bg_color)        # При каждом проходе поверхность заливается выбранным цветом.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        pygame.display.flip()                           # Отображение последнего прорисованного экрана.


if __name__ == "__main__":
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
