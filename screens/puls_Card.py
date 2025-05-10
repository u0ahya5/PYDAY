# screens/puls_Card.py
import pygame

def show_start_screen(screen):
    font = pygame.font.SysFont(None, 72)
    clock = pygame.time.Clock()

    while True:
        screen.fill((30, 30, 30))
        title = font.render("게임 시작 - 엔터키", True, (255, 255, 255))
        screen.blit(title, (200, 250))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "select"
