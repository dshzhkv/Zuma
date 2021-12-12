from game.Params import *
from game.BonusManager import Bonus

BONUS_IMAGES = {Bonus.Pause: {YELLOW: 'images/pause_yellow.png',
                              GREEN: 'images/pause_green.png',
                              BLUE: 'images/pause_blue.png',
                              RED: 'images/pause_red.png'},
                Bonus.Reverse: {YELLOW: 'images/reverse_yellow.png',
                                GREEN: 'images/reverse_green.png',
                                BLUE: 'images/reverse_blue.png',
                                RED: 'images/reverse_red.png'},
                Bonus.Bomb: {YELLOW: 'images/bomb_yellow.png',
                             GREEN: 'images/bomb_green.png',
                             BLUE: 'images/bomb_blue.png',
                             RED: 'images/bomb_red.png'},
                Bonus.Speed: {YELLOW: 'images/speed_yellow.png',
                              GREEN: 'images/speed_green.png',
                              BLUE: 'images/speed_blue.png',
                              RED: 'images/speed_red.png'}}


class Button:
    def __init__(self, button_title, position, width=BTN_WIDTH,
                 height=BTN_HEIGHT, background_color=BROWN, font_color=TAUPE):
        self.title = button_title
        self.font = pygame.font.Font('fonts/Azov.ttf', FONT_SIZE)
        self.title_width, self.title_height = self.font.size(self.title)
        self.center = (position[0], position[1])
        self.width, self.height = width, height
        self.x_start, self.y_start = self.center[0] - self.width // 2, \
                                     self.center[1] - self.height // 2
        self.rect = pygame.Rect((self.x_start, self.y_start,
                                 width, height))
        self.background_color = background_color
        self.font_color = font_color


class Label:
    def __init__(self, text, position, color=BROWN):
        self.font = pygame.font.Font('fonts/Azov.ttf', FONT_SIZE)
        self.color = color
        self.text = self.font.render(text, True, color)
        self.width, self.height = self.font.size(text)
        self.x_start, self.y_start = position[0] - self.width // 2, \
                                     position[1] - self.height // 2

class Display:
    def __init__(self, background_color=TAUPE, buttons=None, labels=None,
                 sprites=None):
        if buttons is None:
            self.buttons = []
        else:
            self.buttons = buttons

        if sprites is None:
            self.spites = []
        else:
            self.spites = sprites

        if labels is None:
            self.labels = []
        else:
            self.labels = labels

        self.background_color = background_color


class UiManager:
    def __init__(self, screen, level):
        self.screen = screen
        self.level = level

        self.start_game_btn = Button('Начать игру', SCREEN_CENTER)
        self.start_game_display = Display(buttons=[self.start_game_btn])

        self.level_label = Label('Уровень {}'.format(level.number),
                                   (WIDTH // 2, 40))
        sprites = [level.player, level.path, level.ball_generator,
                   level.finish, level.shooting_manager]
        self.game_display = Display(sprites=[sprite for sprite in sprites],
                                    labels=[self.level_label])

        self.continue_btn = Button('Продолжить', SCREEN_CENTER)
        self.win_level_display = Display(buttons=[self.continue_btn])

        self.start_level_again_btn = Button('Начать сначала', SCREEN_CENTER,
                                            background_color=TAUPE,
                                            font_color=BROWN)
        self.lose_level_display = Display(BROWN,
                                          buttons=[self.start_level_again_btn])

        self.finish_btn = Button('Закончить', (WIDTH // 2, HEIGHT // 2 +
                                               2 * BTN_HEIGHT))
        self.start_game_again_btn = Button('Начать сначала', SCREEN_CENTER)
        self.win_label = Label('Вы прошли игру!', (WIDTH // 2, HEIGHT // 2 -
                                               2 * BTN_HEIGHT))
        self.win_game_display = Display(buttons=[self.start_game_again_btn,
                                                 self.finish_btn],
                                        labels=[self.win_label])

        self.new_game_button = Button('Новая игра', SCREEN_CENTER,
                                      background_color=TAUPE,
                                      font_color=BROWN)
        self.lose_game_display = Display(BROWN,
                                         buttons=[self.new_game_button])

    def draw_button(self, button):
        width, height = button.width, button.height
        x_start, y_start = button.x_start, button.y_start
        title_params = (x_start + width / 2 - button.title_width / 2,
                        y_start + height / 2 - button.title_height / 2)
        pygame.draw.rect(self.screen, button.background_color,
                         (x_start, y_start, width, height))
        self.screen.blit(button.font.render(button.title, True,
                                            button.font_color), title_params)
        button.rect = pygame.Rect((x_start, y_start, width, height))

    def draw_window(self, window):
        self.screen.fill(window.background_color)
        for button in window.buttons:
            self.draw_button(button)
        for label in window.labels:
            self.put_label(label)
        for sprite in window.spites:
            sprite.draw(self.screen)

    def show_score(self, points):
        points_label = Label('Очки: {}'.format(points), (WIDTH // 4, 40))
        self.put_label(points_label)

    def show_lives(self, lives):

        self.put_label(Label(str(lives), (3 * WIDTH // 4 + 30, 40)))
        self.screen.blit(pygame.transform.smoothscale(
            pygame.image.load("images/life.png"), (20, 20)),
            (3 * WIDTH // 4, 30))

    def put_label(self, label, color=TAUPE):
        pygame.draw.rect(self.screen, color, (label.x_start - label.width / 2,
                                              label.y_start, label.width,
                                              label.height))
        self.screen.blit(label.text, (label.x_start, label.y_start))
