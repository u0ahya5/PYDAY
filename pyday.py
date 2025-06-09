import pygame

# pygame 초기화
pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((640, 480))

# 윈도우 제목 설정
pygame.display.set_caption("Pyday")

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 색깔을 검정으로 설정
    screen.fill((255, 255, 255))

    # 화면 업데이트
    pygame.display.flip()

# pygame 종료
pygame.quit()
