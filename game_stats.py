class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""
 
    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # Игра запускается в неактивном состоянии.
        self.game_active = False
        self.game_active_play = False
        self.game_active_easy = True
        self.game_active_normal = True
        self.game_active_hard = True

        # Рекорд не должен сбрасываться.
        self.high_score = 0
    
    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
