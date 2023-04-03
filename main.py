import pygame, os
from button import Button
from setting_screen import SettingsScreen
from keyconfig import KeyConfig
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Define constants and colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_FONT = pygame.font.Font(None, 36)
TITLE_FONT = pygame.font.Font(None, 72)
key_config = KeyConfig()

# Create a Pygame window and set its title bar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UNO GAME")
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")
icon = pygame.image.load(os.path.join(image_path, "title_image.png"))
pygame.display.set_icon(icon)

# Define the title text and font
title_text = "UNO"
title_surface = TITLE_FONT.render(title_text, True, BLACK)
title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))

# Create three Button instances for the start page
start_button = Button(0.5, 0.5, 0.3, 0.1, "Start", button_color=GREEN)
settings_button = Button(0.5, 0.65, 0.3, 0.1, "Settings", button_color=BLUE)
exit_button = Button(0.5, 0.8, 0.3, 0.1, "Exit", button_color=RED)
start_page_buttons = [start_button, settings_button, exit_button]
focused_index = 0
start_page_buttons[focused_index].focused = True

# resize start page buttons and title when screen size changed

def update_title_text_size():
    global title_surface, title_rect
    screen_width, screen_height = screen.get_size()
    title_font_size = int(screen_height // 8)
    title_font = pygame.font.Font(None, title_font_size)
    title_surface = title_font.render(title_text, True, BLACK)
    title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 6))

update_title_text_size()

def update_start_page_button_sizes():
    for button in start_page_buttons:
        button.update_size()


# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Change size of buttons of start page
        if event.type == VIDEORESIZE:
            update_start_page_button_sizes()
            update_title_text_size()
        # Check for button clicks on the start page
        if start_button.handle_event(event, key_config):
            print("Start button clicked")
        if settings_button.handle_event(event, key_config):
            print("Settings button clicked")
            settings_screen = SettingsScreen(screen, key_config)
            settings_screen.run()
            update_start_page_button_sizes() # update button sizes when returning from setting screen
            update_title_text_size() # update title text size when returning from setting screen
        if exit_button.handle_event(event, key_config):
            print("Exit button clicked")
            running = False

        # Handle keyboard navigation
        focused_index = Button.handle_keyboard_navigation(event, start_page_buttons, focused_index, key_config)
        focused_index = Button.handle_mouse_hover_for_buttons(event, start_page_buttons, focused_index)

    # Draw the title and buttons on the start page
    screen.blit(title_surface, title_rect)
    start_button.draw(screen)
    settings_button.draw(screen)
    exit_button.draw(screen)

    # Draw an additional black border around the focused button
    if start_page_buttons[focused_index].focused:
        pygame.draw.rect(screen, BLACK, start_page_buttons[focused_index].rect.inflate(6, 6), 3)

    pygame.display.flip()

pygame.quit()






