from Params import *


class Button:
    def __init__(self, button_title, position, width=BTN_WIDTH,
                 height=BTN_HEIGHT, background_color=BLACK, font_color=WHITE):
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


class Window:
    def __init__(self, background_color=WHITE, buttons=None, sprites=None):
        if buttons is None:
            self.buttons = []
        else:
            self.buttons = buttons

        if sprites is None:
            self.spites = []
        else:
            self.spites = sprites

        self.background_color = background_color



class UiManager:
    def __init__(self, screen, *sprites):
        self.screen = screen

        self.start_game_btn = Button('Начать игру', SCREEN_CENTER)
        self.start_window = Window(buttons=[self.start_game_btn])

        self.game_window = Window(TAUPE, sprites=[sprite for sprite in
                                                  sprites])

        self.continue_btn = Button('Продолжить', SCREEN_CENTER)
        self.win_window = Window(buttons=[self.continue_btn])

        self.start_again_btn = Button('Начать сначала', SCREEN_CENTER,
                                      background_color=WHITE, font_color=BLACK)
        self.lose_window = Window(BLACK, buttons=[self.start_again_btn])

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
        for sprite in window.spites:
            sprite.draw(self.screen)

