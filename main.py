import pygame
import sys #인터프리터와 관련된 기능을 제공하는 모듈

pygame.init()
pygame.display.set_caption("PYDAY")
clock = pygame.time.Clock()

screen = pygame.display.set_mode((600, 700))  # Figma 기준 화면 사이즈

logo = pygame.image.load("pythonimg/logo.png")
play = pygame.image.load("pythonimg/playbut.png")
exit = pygame.image.load("pythonimg/exitbut.png")

# 크기 조절 (원본 이미지 사이즈 유지 가능, 또는 조정)
logo = pygame.transform.scale(logo, (336, 256))
playbut = pygame.transform.scale(play, (170, 65))
exitbut = pygame.transform.scale(exit, (150, 65))

# 중앙 기준 위치 계산
screen_width = 600
center_x = screen_width // 2

# 위치 설정 (센터 기준, 더 아래로 이동)
logo_rect = logo.get_rect(center=(center_x, 220))        # 로고 아래로
playbut_rect = playbut.get_rect(center=(center_x, 430))  # Play 아래로
exitbut_rect = exitbut.get_rect(center=(center_x, 510))  # Exit 아래로
# 배경색
background_color = (247, 240, 232, 100)

def main():
    running = True
    while running:
        screen.fill(background_color)

        screen.blit(logo, logo_rect) #로고출력

        # 이미지 그리기
        screen.blit(playbut, playbut_rect)
        screen.blit(exitbut, exitbut_rect)

        pygame.display.flip() #화면에 그린 내용을 반영함
        clock.tick(60) #1초 최대 60프레임

        for event in pygame.event.get(): #pygame의 이벤트는 여기서 실행, 움직임 감지
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    print("다음 화면으로 이동합니다.")
                    # 예시: 여기서 새로운 함수 호출 또는 상태 전환 가능
                elif exit_rect.collidepoint(event.pos):
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()