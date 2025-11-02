class GameStats:
    """Статистика игры Alien Invasion."""

    def __init__(self, ai_game):
        """Инициализируем статистику."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0                         # Рекорд не должен сбрасываться.

    def reset_stats(self):
        """Инициализируем статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
