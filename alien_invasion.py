import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from difficulty.button_play import Button_Play
from difficulty.button_easy import Button_Easy
from difficulty.button_norm import Button_Norm
from difficulty.button_hard import Button_Hard
from ship import Ship
from bullets.bullet import Bullet
from bullets.bullet_alien import Bullet_Alien
from alien import Alien


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляра для хранения игровой статистики
        # и панели результатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets_ship = pygame.sprite.Group()
        self.bullets_alien = pygame.sprite.Group()
        self.alien = pygame.sprite.Group()

        self._create_fleet()

        # Создание кнопки Play.
        self.play_button = Button_Play(self, 'Play')

        # Создание кнопки Play.
        self.easy_button = Button_Easy(self, 'Easy')

        # Создание кнопки Normal
        self.normal_button = Button_Norm(self, 'Normal')

        # Создание кнопки Normal
        self.hard_button = Button_Hard(self, 'Hard')

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets_ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_easy_button(mouse_pos)
                self._check_normal_button(mouse_pos)
                self._check_hard_button(mouse_pos)
            # Отображение последнего прорисованного экрана.
            pygame.display.flip()
    
    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked_play = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked_play and not self.stats.game_active:
            self.stats.game_active_play = True
            self.stats.game_active_easy = False
            self.stats.game_active_normal = False
            self.stats.game_active_hard = False
            self._check_easy_button(mouse_pos)
            self._check_normal_button(mouse_pos)
            self._check_hard_button(mouse_pos)

    def _check_easy_button(self, mouse_pos):
        button_clicked_easy = self.easy_button.rect.collidepoint(mouse_pos)
        if button_clicked_easy and not self.stats.game_active and not self.stats.game_active_easy:
            # Сброс игровых настроек.              
            self.settings.initialize_dynamic_settings()
            # Сброс игровой статистики.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.stats.game_active_easy = True
            self.stats.game_active_normal = True
            self.stats.game_active_hard = True
            self.sb.prep_score()    
            self.sb.prep_level()
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов.
            self.alien.empty()
            self.bullets_ship.empty()
            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Указатель мыши скрывается.
            pygame.mouse.set_visible(False)
    
    def _check_normal_button(self, mouse_pos):
        button_clicked_normal = self.normal_button.rect.collidepoint(mouse_pos)
        if button_clicked_normal and not self.stats.game_active and not self.stats.game_active_normal:
            # Сброс игровых настроек.              
            self.settings.initialize_dynamic_settings()
            # Сброс игровой статистики.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.stats.game_active_easy = True
            self.stats.game_active_normal = True
            self.stats.game_active_hard = True
            self.sb.prep_score()    
            self.sb.prep_level()
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов.
            self.alien.empty()
            self.bullets_ship.empty()
            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()
            self.settings.alien_speed_factor += 2

            # Указатель мыши скрывается.
            pygame.mouse.set_visible(False)

    def _check_hard_button(self, mouse_pos):
        button_clicked_hard = self.hard_button.rect.collidepoint(mouse_pos)
        if button_clicked_hard and not self.stats.game_active and not self.stats.game_active_hard:
            # Сброс игровых настроек.              
            self.settings.initialize_dynamic_settings()
            # Сброс игровой статистики.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.stats.game_active_easy = True
            self.stats.game_active_normal = True
            self.stats.game_active_hard = True
            self.sb.prep_score()    
            self.sb.prep_level()
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов.
            self.alien.empty()
            self.bullets_ship.empty()
            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()
            self.settings.alien_speed_factor += 4

            # Указатель мыши скрывается.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets_ship) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets_ship.add(new_bullet)
    
    def _fire_bullet_alien(self):
        #Создание нового снаряда пришельца и включение его в группу bullets.
        if len(self.bullets_alien) < self.settings.bullets_alien_allowed:
            new_bullet = Bullet_Alien(self)
            self.bullets_alien.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.bullets_ship.update()

        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets_ship.copy():
            if bullet.rect.bottom <= 0:
                self.bullets_ship.remove(bullet)
        
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        # Проверка попаданий в пришельцев.
        # При обнаружении попадания удалить снаряд и пришельца.
        collisions = pygame.sprite.groupcollide(
            self.bullets_ship, self.alien, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.alien:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets_ship.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня.
            self.stats.level += 1
            self.sb.prep_level()

        return collisions

    def _update_aliens(self):
        """
        Проверяет, достиг ли флот края экрана,
        с последующим обновлением позиций всех пришельцев во флоте.
        """
        self._check_fleet_edges()
        self.alien.update()

        # Проверка коллизий "пришелец — корабль".
        if pygame.sprite.spritecollideany(self.ship, self.alien):
            self._ship_hit()
        
        # Проверить, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()
    
    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()
 
            # Очистка списков пришельцев и снарядов.
            self.alien.empty()
            self.bullets_ship.empty()
 
            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()
 
            # Пауза.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.alien.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.alien.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.alien.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание пришельца и вычисление количества пришельцев в ряду
        # Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (4 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота вторжения.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.alien.add(alien)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets_ship.sprites():
            bullet.draw_bullet()
        self.alien.draw(self.screen)

        # Вывод информации о счете.
        self.sb.show_score()

        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_active_play:
            self.play_button.draw_buttom()
        
        # Кнопка Easy отображается в том случае, если игра неактивна.
        if not self.stats.game_active_easy:
            self.easy_button.draw_buttom()
        
        # Кнопка Easy отображается в том случае, если игра неактивна.
        if not self.stats.game_active_normal:
            self.normal_button.draw_buttom()

        # Кнопка Easy отображается в том случае, если игра неактивна.
        if not self.stats.game_active_hard:
            self.hard_button.draw_buttom()    

        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
