import pygame
import sys
from screens.gamelist import show_game_select_screen

pygame.init()
pygame.display.set_caption("PYDAY")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 600))

background_color = (247, 240, 232)

logo = pygame.image.load("pythonimg/logo.png")
play_img = pygame.image.load("pythonimg/playbut.png")
exit_img = pygame.image.load("pythonimg/exitbut.png")

logo = pygame.transform.scale(logo, (336, 256))
play_button = pygame.transform.scale(play_img, (170, 65))
exit_button = pygame.transform.scale(exit_img, (150, 65))

center_x = screen.get_width() // 2
logo_rect = logo.get_rect(center=(center_x, 220))
play_rect = play_button.get_rect(center=(center_x, 430))
exit_rect = exit_button.get_rect(center=(center_x, 510))

def main():
    running = True
    while running:
        screen.fill(background_color)

        screen.blit(logo, logo_rect)
        screen.blit(play_button, play_rect)
        screen.blit(exit_button, exit_rect)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    show_game_select_screen(screen)
                    running = False
                elif exit_rect.collidepoint(event.pos):
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()