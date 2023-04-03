import pygame, os
from button import Button
from setting_screen import SettingsScreen
from pygame.locals import *

pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 초기 창 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 폰트
BUTTON_FONT = pygame.font.Font(None, 36)
TITLE_FONT = pygame.font.Font(None, 72)

# 창 생성 및 제목 표시줄 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UNO GAME")
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")
icon = pygame.image.load(os.path.join(image_path, "title_image.png"))
pygame.display.set_icon(icon)

# 제목 텍스트, 폰트 정의
title_text = "UNO"
title_surface = TITLE_FONT.render(title_text, True, BLACK)
title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))

# 시작 페이지 버튼 생성
start_button = Button(0.5, 0.5, 0.3, 0.1, "Start", button_color=GREEN)
settings_button = Button(0.5, 0.65, 0.3, 0.1, "Settings", button_color=BLUE)
exit_button = Button(0.5, 0.8, 0.3, 0.1, "Exit", button_color=RED)
start_page_buttons = [start_button, settings_button, exit_button]
focused_index = 0
start_page_buttons[focused_index].focused = True

# 화면 크기 변경되면 시작 페이지 버튼 및 제목 크기 조정

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

        # 시작 페이지 버튼 크기 변경
        if event.type == VIDEORESIZE:
            update_start_page_button_sizes()
            update_title_text_size()
        # 시작 페이지 버튼 클릭 확인
        if start_button.handle_event(event):
            print("Start button clicked")
        if settings_button.handle_event(event):
            settings_screen = SettingsScreen(screen)
            settings_screen.run()
            update_start_page_button_sizes() # 버튼 크기 재설정
            update_title_text_size() # 제목 크기 재설정
        if exit_button.handle_event(event):
            print("Exit button clicked")
            running = False

        # 키보드 navi, 마우스 호버 처리
        focused_index = Button.handle_keyboard_navigation(event, start_page_buttons, focused_index)
        focused_index = Button.handle_mouse_hover_for_buttons(event, start_page_buttons, focused_index)

    # 제목, 버튼 그리기
    screen.blit(title_surface, title_rect)
    start_button.draw(screen)
    settings_button.draw(screen)
    exit_button.draw(screen)

    # 포커스 버튼 테두리 그리기
    if start_page_buttons[focused_index].focused:
        pygame.draw.rect(screen, BLACK, start_page_buttons[focused_index].rect.inflate(6, 6), 3)

    pygame.display.flip()

pygame.quit()






