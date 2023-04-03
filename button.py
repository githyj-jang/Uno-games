import pygame
from keyconfig import KeyConfig
from pygame.locals import *

pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 폰트 초기화
pygame.font.init()
BUTTON_FONT = pygame.font.SysFont('Arial', 24)


class Button:
    def __init__(self, x_ratio, y_ratio, width_ratio, height_ratio, text, button_color=WHITE, text_color=BLACK, y_offset=0):
        self.x_ratio = x_ratio
        self.y_ratio = y_ratio
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        self.button_color = button_color
        self.text_color = text_color
        self.y_offset = y_offset
        self.text = text
        self.hover = False
        self.focused = False
        self.text_surface = BUTTON_FONT.render(self.text, True, self.text_color)
        self.update_size()

    def update_size(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.width = int(screen_width * self.width_ratio)
        self.height = int(screen_height * self.height_ratio)
        self.x = int(screen_width * self.x_ratio) - int(self.width / 2)
        self.y = int(screen_height * self.y_ratio) - int(self.height / 2) + self.y_offset  # 버튼 상하 위치 조절
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_surface = BUTTON_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def handle_keyboard_navigation(event, buttons, focused_index, key_config):
        if event.type == pygame.KEYDOWN:
            if event.key == key_config.get_key("up") or event.key == key_config.get_key("down"):
                # Unfocus the current button
                buttons[focused_index].focused = False
                
                # Update the focused_index based on the key pressed
                if event.key == key_config.get_key("up"):
                    focused_index -= 1
                elif event.key == key_config.get_key("down"):
                    focused_index += 1
                
                # Keep the index within the range of buttons
                focused_index %= len(buttons)
                
                # Focus the new button
                buttons[focused_index].focused = True
            elif event.key == key_config.get_key("enter"):
                if buttons[focused_index].handle_event(event):
                    print(f"Button {focused_index} pressed")
        return focused_index
    
    def handle_mouse_hover_for_buttons(event, buttons, focused_index):
        if event.type == pygame.MOUSEMOTION:
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    if not button.focused:
                        buttons[focused_index].focused = False
                        button.focused = True
                        return buttons.index(button)
                elif button.focused and not any(btn.hover for btn in buttons):
                    button.focused = False
        return focused_index
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.button_color, self.rect)
        if self.hover:
            pygame.draw.rect(surface, self.text_color, self.rect, 2)  # Draw border for hovered button
        if self.focused:  # Draw an additional border for the focused button
            pygame.draw.rect(surface, self.text_color, self.rect.inflate(6, 6), 3)
        surface.blit(self.text_surface, self.text_rect)

    def handle_event(self, event, key_config):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        elif event.type == key_config.get_key("enter"):  # Updated this line
            if self.focused:
                return True
        return False

