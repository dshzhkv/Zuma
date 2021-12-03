from Params import *


class Button:
    def __init__(self, button_title, position, width=BTN_WIDTH,
                 height=BTN_HEIGHT, color=BLACK):
        self.title = button_title
        self.font = pygame.font.Font('fonts/Azov.ttf', FONT_SIZE)
        self.title_width, self.title_height = self.font.size(self.title)
        self.center = (position[0], position[1])
        self.width, self.height = width, height
        self.rect = pygame.Rect((self.center[0], self.center[1],
                                 width, height))
        self.color = color


class Window:
    def __init__(self, background_color=WHITE):
        self.buttons = []
        self.labels = []
        self.spites = []
        self.background_color = background_color

    def add_buttons(self, *buttons):
        self.buttons += [button for button in buttons]

    def add_labels(self, *labels):
        self.labels += [label for label in labels]

    def add_sprites(self, *sprites):
        self.spites += [sprite for sprite in sprites]


class UiManager:
    def __init__(self, screen, *sprites):
        self.screen = screen

        self.start_window = Window()
        self.start_game_btn = Button('Начать игру', (WIDTH // 2, HEIGHT // 2))
        self.start_window.add_buttons(self.start_game_btn)

        self.game_window = Window(BLACK)
        for sprite in sprites:
            self.game_window.add_sprites(sprite)

    def draw_button(self, button):
        width, height = button.width, button.height
        x_start, y_start = button.center[0] - button.width // 2, \
                           button.center[1] - button.height // 2
        title_params = (x_start + width / 2 - button.title_width / 2,
                        y_start + height / 2 - button.title_height / 2)
        pygame.draw.rect(self.screen, button.color, (x_start, y_start, width,
                                                     height))
        self.screen.blit(button.font.render(button.title, True, WHITE),
                         title_params)
        button.rect = pygame.Rect((x_start, y_start, width, height))

    def draw_window(self, window):
        self.screen.fill(window.background_color)
        for button in window.buttons:
            self.draw_button(button)
        for sprite in window.spites:
            sprite.draw(self.screen)

