import pygame
from button import Button


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WINDOW_SIZES = [(640, 480), (800, 600), (1280, 720)]
TITLE_FONT = pygame.font.Font(None, 72)
TITLE_TEXT = "UNO"

class SettingsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.title_text = "UNO"
        self.running = True
        self.settings_buttons = [
            Button(0.5, 0.3, 0.4, 0.1, "Window Size", button_color=BLUE, text_color=WHITE),
            Button(0.5, 0.45, 0.4, 0.1, "Key Setting", button_color=BLUE, text_color=WHITE),
            Button(0.5, 0.6, 0.4, 0.1, "Color Weakness Mode", button_color=BLUE, text_color=WHITE),
            Button(0.5, 0.75, 0.4, 0.1, "Default", button_color=BLUE, text_color=WHITE),
            Button(0.5, 0.9, 0.4, 0.1, "Back", button_color=BLUE, text_color=WHITE)
        ]

        self.window_size_index = 0
        self.focused_index = 0
        self.settings_buttons[self.focused_index].focused = True
        self.update_title_text()

    def change_window_size(self, size):
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("UNO Start Page")
        for button in self.settings_buttons:
            button.update_size()
        self.update_title_text()

    def update_title_text(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.title_surface = TITLE_FONT.render(self.title_text, True, BLACK)
        self.title_rect = self.title_surface.get_rect(center=(screen_width // 2, screen_height // 6))

    def run(self):

        running = True
        focused_index = 0  # Initialize focused_index
        self.settings_buttons[focused_index].focused = True

        while running:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                for button in self.settings_buttons:
                    if button.handle_event(event):
                        print(f"{button.text} button clicked")
                        if button == self.settings_buttons[0]:
                            self.window_size_index = (self.window_size_index + 1) % len(WINDOW_SIZES)
                            self.change_window_size(WINDOW_SIZES[self.window_size_index])
                            button.text = f"Window Size: {WINDOW_SIZES[self.window_size_index][0]}x{WINDOW_SIZES[self.window_size_index][1]}"
                            button.update_size()
                        elif button == self.settings_buttons[-1]:
                            self.running = False
                new_focused_index = Button.handle_keyboard_navigation(event, self.settings_buttons, self.focused_index)
                focused_index = Button.handle_mouse_hover_for_buttons(event, self.settings_buttons, focused_index)
                back_button = self.settings_buttons[-1]
                if back_button.handle_event(event):
                    running = False
                if new_focused_index != self.focused_index:
                    self.settings_buttons[self.focused_index].focused = False
                    self.focused_index = new_focused_index
                    self.settings_buttons[self.focused_index].focused = True
            for button in self.settings_buttons:
                button.update_size()
            screen_width, screen_height = pygame.display.get_surface().get_size()
            title_surface = TITLE_FONT.render(TITLE_TEXT, True, BLACK)
            title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 6))
            self.update_title_text()
            self.screen.blit(self.title_surface, self.title_rect)
            for button in self.settings_buttons:
                button.draw(self.screen)
                if button.focused:
                    pygame.draw.rect(self.screen, BLACK, button.rect.inflate(6, 6), 3)


            pygame.display.flip()

        return True