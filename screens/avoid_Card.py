import pygame
import random
import sys
import json
import os

WIDTH, HEIGHT = 500, 600
FPS = 60

WHITE = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0, 180)
COLLIDE_MARGIN = 15

HIGH_SCORE_FILE = "high_score.json"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("독사과 피하기")
clock = pygame.time.Clock()
main_font = pygame.font.SysFont(None, 35)
title_font = pygame.font.SysFont(None, 70)

# 그림자 오버레이
shadow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
shadow_surf.fill(SHADOW_COLOR)

background = pygame.image.load("pythonimg/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player_img = pygame.image.load("pythonimg/pie.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (100, 60))
sun_img = pygame.image.load("pythonimg/sun.png").convert_alpha()
sun_img = pygame.transform.scale(sun_img, (70, 70))
poison_img = pygame.image.load("pythonimg/poison_apple.png").convert_alpha()
poison_img = pygame.transform.scale(poison_img, (50, 50))

start_img = pygame.image.load("pythonimg/startbut.png").convert_alpha()
start_img = pygame.transform.scale(start_img, (170, 65))
exit_img = pygame.image.load("pythonimg/exitbut.png").convert_alpha()
exit_img = pygame.transform.scale(exit_img, (150, 65))

# 최고점 불러오기 & 저장하기
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            data = json.load(f)
            return data.get("avoid_game", 0)
    except:
        return 0

def save_high_score(score):
    data = {}
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            data = json.load(f)
    data["avoid_game"] = score
    with open(HIGH_SCORE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def game_over_screen(score, high_score):
    from screens.gamelist import show_game_select_screen
    start_rect = start_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    exit_rect = exit_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 160))

    while True:
        mouse = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                show_game_select_screen(screen)
                return False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if start_rect.collidepoint(mouse):
                    return True
                if exit_rect.collidepoint(mouse):
                    return False

        screen.blit(background, (0, 0))
        screen.blit(shadow_surf, (0, 0))
        over = title_font.render("Game Over", True, WHITE)
        sc_txt = main_font.render(f"Score: {score}", True, WHITE)
        hi_txt = main_font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(over, over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
        screen.blit(sc_txt, sc_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        screen.blit(hi_txt, hi_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(start_img, start_rect)
        screen.blit(exit_img, exit_rect)
        pygame.display.flip()
        clock.tick(FPS)

def main():
    from screens.gamelist import show_game_select_screen
    score = 0
    high_score = load_high_score()
    player_rect = player_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 55))
    suns, poisons = [], []
    timer = 0

    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                show_game_select_screen(screen)
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += 5

        #아이템 소환
        timer += 1
        if timer >= 30:
            timer = 0
            if random.random() < 0.7:
                rect = poison_img.get_rect(
                    x=random.randint(0, WIDTH - poison_img.get_width()),
                    y=-poison_img.get_height()
                )
                poisons.append(rect)
            else:
                rect = sun_img.get_rect(
                    x=random.randint(0, WIDTH - sun_img.get_width()),
                    y=-sun_img.get_height()
                )
                suns.append(rect)

        # 충돌 처리 & 이동
        for arr, speed, add in ((suns, 4, 10), (poisons, 6, 0)):
            for r in arr[:]:
                r.y += speed
                if r.top > HEIGHT:
                    arr.remove(r)
                elif r.inflate(-COLLIDE_MARGIN, -COLLIDE_MARGIN).colliderect(player_rect):
                    if add > 0:
                        score += add
                        arr.remove(r)
                    else:
                        if score > high_score:
                            high_score = score
                            save_high_score(high_score)
                        go_again = game_over_screen(score, high_score)
                        if go_again:
                            return main()
                        else:
                            show_game_select_screen(screen)
                            return


        screen.blit(background, (0, 0))
        screen.blit(player_img, player_rect)
        for r in suns:
            screen.blit(sun_img, r)
        for r in poisons:
            screen.blit(poison_img, r)
        screen.blit(main_font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(main_font.render(f"High Score: {high_score}", True, WHITE), (10, 50))
        pygame.display.flip()

def start_avoid_game():
    main()

if __name__ == '__main__':
    main()
