import pygame
from button import Button

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# 창 크기 옵션 정의
WINDOW_SIZES = [(640, 480), (800, 600), (1280, 720)]

# 제목 폰트와 텍스트 정의
TITLE_FONT = pygame.font.Font(None, 72)
TITLE_TEXT = "UNO"

class SettingsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.title_text = "UNO"
        self.running = True

        # 설정 화면에 표시될 버튼 리스트
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

    # 창 크기 변경 메소드
    def change_window_size(self, size):
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("UNO Start Page")
        for button in self.settings_buttons:
            button.update_size()
        self.update_title_text()

    # 제목 텍스트 위치 업데이트
    def update_title_text(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.title_surface = TITLE_FONT.render(self.title_text, True, BLACK)
        self.title_rect = self.title_surface.get_rect(center=(screen_width // 2, screen_height // 6))

    # 설정 화면 메인 루프
    def run(self):

        running = True
        focused_index = 0  # 포커스 초기화
        self.settings_buttons[focused_index].focused = True

        while running:
            self.screen.fill(WHITE)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return False
                
                # 각 버튼 이벤트 처리
                for button in self.settings_buttons:

                    if button.handle_event(event):
                        print(f"{button.text} button clicked")
                        
                        # 창 크기 변경
                        if button == self.settings_buttons[0]:
                            self.window_size_index = (self.window_size_index + 1) % len(WINDOW_SIZES)
                            self.change_window_size(WINDOW_SIZES[self.window_size_index])
                            button.text = f"Window Size: {WINDOW_SIZES[self.window_size_index][0]}x{WINDOW_SIZES[self.window_size_index][1]}"
                            button.update_size()
                        
                        # 뒤로가기
                        elif button == self.settings_buttons[-1]:
                            self.running = False
                # 키보드 navi 처리
                new_focused_index = Button.handle_keyboard_navigation(event, self.settings_buttons, self.focused_index)
                # 마우스 호버 처리
                focused_index = Button.handle_mouse_hover_for_buttons(event, self.settings_buttons, focused_index)
                back_button = self.settings_buttons[-1]

                # 뒤로가기 버튼 클릭 처리
                if back_button.handle_event(event):
                    running = False


                # 포커스 업데이트
                if new_focused_index != self.focused_index:
                    self.settings_buttons[self.focused_index].focused = False
                    self.focused_index = new_focused_index
                    self.settings_buttons[self.focused_index].focused = True
            
            # 버튼 크기 업데이트
            for button in self.settings_buttons:
                button.update_size()

            # 화면 크기 업데이트
            screen_width, screen_height = pygame.display.get_surface().get_size()
            title_surface = TITLE_FONT.render(TITLE_TEXT, True, BLACK)
            title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 6))
            
            # 제목 텍스트 업데이트 및 화면에 띄우기
            self.update_title_text()
            self.screen.blit(self.title_surface, self.title_rect)

            # 모든 버튼 그리기
            for button in self.settings_buttons:
                button.draw(self.screen)

                # 포커스 버튼 테두리 그리기
                if button.focused:
                    pygame.draw.rect(self.screen, BLACK, button.rect.inflate(6, 6), 3)


            pygame.display.flip()

        return True