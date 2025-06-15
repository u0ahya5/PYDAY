import pygame
import random
import sys
import time
import json
import os

pygame.init()

WIDTH, HEIGHT = 500, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("사과 클릭 팝")

main_font = pygame.font.SysFont(None, 35)
title_font = pygame.font.SysFont(None, 70)

red_apple_img = pygame.image.load("pythonimg/apple.png").convert_alpha()
red_apple_img = pygame.transform.scale(red_apple_img, (70, 70))

poison_apple_img = pygame.image.load("pythonimg/poison_apple.png").convert_alpha()
poison_apple_img = pygame.transform.scale(poison_apple_img, (70, 70))

start_img = pygame.image.load("pythonimg/startbut.png").convert_alpha()
start_img = pygame.transform.scale(start_img, (170, 65))

exit_img = pygame.image.load("pythonimg/exitbut.png").convert_alpha()
exit_img = pygame.transform.scale(exit_img, (150, 65))

background_surface = pygame.Surface((WIDTH, HEIGHT))
background_surface.fill((255, 255, 255))

shadow_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
shadow_overlay.fill((0, 0, 0, 128))

# 최고점 불러오기 & 저장하기
score_file_path = "high_score.json"

def load_high_score():
    if os.path.exists(score_file_path):
        with open(score_file_path, "r") as file:
            data = json.load(file)
            return data.get("appleclick_game", 0)
    return 0

def save_high_score(new_score):
    data = {}
    if os.path.exists(score_file_path):
        with open(score_file_path, "r") as file:
            data = json.load(file)
    data["appleclick_game"] = new_score
    with open(score_file_path, "w") as file:
        json.dump(data, file, indent=4)

def show_game_over_screen(final_score, best_score):
    clock = pygame.time.Clock()
    start_button_rect = pygame.Rect(0, 0, 150, 50)
    exit_button_rect = pygame.Rect(0, 0, 150, 50)
    start_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 80)
    exit_button_rect.center = (WIDTH // 2 + 10, HEIGHT // 2 + 160)

    while True:
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(mouse_position):
                    return True  
                if exit_button_rect.collidepoint(mouse_position):
                    return False  

        screen.fill((0, 0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        game_over_text = title_font.render("Game Over", True, (255, 255, 255))
        score_text = main_font.render(f"Score: {final_score}", True, (255, 255, 255))
        high_score_text = main_font.render(f"High Score: {best_score}", True, (255, 255, 255))

        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        screen.blit(high_score_text, high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        if start_img:
            screen.blit(start_img, start_button_rect)
        if exit_img:
            screen.blit(exit_img, exit_button_rect)

        pygame.display.flip()
        clock.tick(60)

def run_game():
    current_score = 0
    highest_score = load_high_score()
    game_start_time = time.time()
    apple_list = []
    last_apple_spawn_time = time.time()
    total_game_duration = 30

    while True:
        current_time = time.time()
        elapsed_time = current_time - game_start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                from screens.gamelist import show_game_select_screen
                show_game_select_screen(screen)
                return 0, highest_score, False  
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for apple in apple_list[:]:
                    if apple[3].collidepoint(pos):
                        if apple[2] == 'red':
                            current_score += 10
                        else:
                        
                            if current_score == 0:
                                if current_score > highest_score:
                                    highest_score = current_score
                                    save_high_score(highest_score)
                                return current_score, highest_score, True
                            current_score = max(0, current_score - 10)
                        apple_list.remove(apple)
                        break

        if current_time - last_apple_spawn_time > 0.5:
            apple_color = random.choice(['red', 'green'])
            apple_image = red_apple_img if apple_color == 'red' else poison_apple_img
            x_position = random.randint(0, WIDTH - 70)
            y_position = random.randint(150, HEIGHT - 70)
            apple_rect = pygame.Rect(x_position, y_position, 70, 70)
            spawn_time = current_time
            apple_list.append([x_position, y_position, apple_color, apple_rect, spawn_time])
            last_apple_spawn_time = current_time

        apple_list = [apple for apple in apple_list if current_time - apple[4] < 1.5]

        #타임 오버 되면
        if elapsed_time >= total_game_duration:
            if current_score > highest_score:
                highest_score = current_score
                save_high_score(highest_score)
            return current_score, highest_score, True  

        screen.blit(background_surface, (0, 0))
        for apple in apple_list:
            image_to_draw = red_apple_img if apple[2] == 'red' else poison_apple_img
            screen.blit(image_to_draw, (apple[0], apple[1]))

        remaining_time = max(0, int(total_game_duration - elapsed_time))
        timer_display = main_font.render(f"Time: {remaining_time}", True, (242, 63, 59))
        score_display = main_font.render(f"Score: {current_score}", True, (0, 0, 0))
        high_score_display = main_font.render(f"High Score: {highest_score}", True, (0, 0, 0))

        screen.blit(timer_display, (20, 20))
        screen.blit(score_display, (20, 70))
        screen.blit(high_score_display, (20, 120))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def start_appleclick_game(screen):
    while True:
        final_score, best_score, completed = run_game()
        if not completed:
            return 
        play_again = show_game_over_screen(final_score, best_score)
        if play_again:
            continue
        else:
            from screens.gamelist import show_game_select_screen
            show_game_select_screen(screen)
            return