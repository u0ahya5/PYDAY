from selectors import SelectSelector

import pygame
import random

WIDTH = 600
Grid_offset_y = 100

# 초기 설정
pygame.init()
screen = pygame.display.set_mode((600, 700)) # 창 크기 설정
pygame.display.set_caption("Apple Game") # 윈도우 이름 설정
clock = pygame.time.Clock() # 시간 카운트 다운
font = pygame.font.Font(None, 36) #기본 폰트, 크기 36짜리 사용

# 사과 설정
Cell_size = 60 # 셀 사이즈
rows = 10 # 가로 (행)
cols = 8 # 세로 (열)
empty = 100 # 빈 공간 (위에 점수/시간 표시 공간)

# 사과 클래스
class Apple:
    def __init__ (self, x, y, value):
        self.rect = pygame.Rect(x, y, Cell_size, Cell_size)
        self.value = value
        self.selected = False
    def draw(self, surface):
        color = (255, 100, 100) if not self.selected else (255, 0, 0) # 이건 무슨 말이지?
        pygame.draw.ellipse(surface, color, self.rect) # ellipse 이게 뭐지?
        txt = font.render(str(self.value), True, (0, 0, 0))
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect) # blit가 뭐지

# 사과 격자 만들기
def create_apples():
    apples = []
    for row in range(rows):
        for col in range(cols):
            x = col * Cell_size + (WIDTH - cols * Cell_size) // 2
            y = row * Cell_size + Grid_offset_y # 이건 또 뭐여
            value = random.randint(1, 9) # 1이랑 9사이 랜덤 정수?
            apples.append(Apple(x, y, value)) # apples 배열에 Apple 값을 넣는다?
    return apples

apples = create_apples()

# 게임 루프
running = True
while running:
    screen.fill((255, 255, 255)) # 255, 255, 255 색으로 채운듯?

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 사과 그리기
    for apple in apples:
        apple.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()