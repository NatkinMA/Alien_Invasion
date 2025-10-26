class Settings:
    """Класс для хранения настроек игры Alien Invasion"""
    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # Настройки корабля.
        self.ship_speed = 1.5
        # Параметры снаряда.
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 10
        # Настройки пришельцев.
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1            # Направление движения флота пришельцев: 1 - вправо, -1 - влево.
