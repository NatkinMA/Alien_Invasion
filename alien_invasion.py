import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.clock = pygame.time.Clock()                # Объект для отслеживания игрового времени.
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        self.stats = GameStats(self)                    # Статистика игры.

        """
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        """
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        # Устанавливаем флаг активного состояния игры.
        self.game_active = False
        # Создаем кнопку Play.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Запускает основной цикл игры."""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def start_game(self):
        # Сброс игровой статистики.
        self.stats.reset_stats()
        self.game_active = True

        # Очистка групп aliens и bullets.
        self.bullets.empty()
        self.aliens.empty()

        # Создаем новый флот и размещаем корабль в центре.
        self._create_fleet()
        self.ship.center_ship()
        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)

    def _check_play_button(self, mouse_pos):
        """Запускаем новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings() # Сброс игровых настроек.
            self.start_game()

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
        elif event.key == pygame.K_p:
            self.start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создаем новый снаряд и добавляем его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self))

    def _check_bullet_alien_collisions(self):
        """Обрабатываем коллизии снарядов с пришельцами."""
        # Удаляем снаряды и пришельцев, участвующих в коллизиях.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_bullets(self):
        """Обновляем позиции снарядов и удаляем снаряды, достигшие верхней границы экрана."""
        # Обновление позиций снарядов.
        self.bullets.update()
        # Удаляем снаряды, вышедшие за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
#        print(len(self.bullets))

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Проверяем положение пришельца, достиг ли он края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self):
        """Обрабатываем столкновение корабля с пришельцем."""
        if self.stats.ships_left > 0:
            # Уменьшаем ships_left.
            self.stats.ships_left -= 1
            # Очищаем группы aliens и bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Создаем новый флот и корабль, который размещаем в исходных позициях.
            self._create_fleet()
            self.ship.center_ship()
            # Пауза.
            sleep(1.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверка достижения пришельцами нижнего края экрана."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Считаем, что корабль поражен.
                self._ship_hit()
                break

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте.
        Проверяет, достиг ли флот края экрана и обновляет позиции всех пришельцев."""
        self._check_fleet_edges()
        self.aliens.update()
        # Проверка коллизий "пришелец - корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Проверить столкновение пришельцев с нижним краем экрана.
        self._check_aliens_bottom()
#            print("Ship hit!!!")

    def _create_fleet(self):
        """Создаем флот пришельцев."""
        # Создание пришельца и вычисление количества пришельцев в ряду.
        # Интервал между соседними пришельцами равен ширине пришельца.
        # Расстояние между пришельцами составляет одну ширину
        # и одну высоту пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Конец ряда: сбрасываем значение x и инкрементируем значение y.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_screen(self):
        """Обновление изображения на экране и отображение нового экрана."""
        self.screen.fill(self.settings.bg_color)        # При каждом проходе поверхность заливается выбранным цветом.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        if not self.game_active:                        # Если игра неактивна
            self.play_button.draw_button()              # отображаем кнопку "Play".

        pygame.display.flip()                           # Отображение последнего прорисованного экрана.


if __name__ == "__main__":
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
