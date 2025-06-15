import pygame
import random
import time
import sys
import json
import os

pygame.init()

# 화면 크기
WIDTH = 500
HEIGHT = 600
TOP_AREA = 50
CELL_SIZE = 45

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puls Card Game")

main_font = pygame.font.SysFont(None, 35)
apple_font = pygame.font.SysFont(None, 25)
title_font = pygame.font.SysFont(None, 70)

cols = WIDTH // CELL_SIZE
rows = (HEIGHT - TOP_AREA) // CELL_SIZE

time_limit = 120

apple_img = None
if os.path.exists("pythonimg/apple.PNG"):
    apple_img = pygame.image.load("pythonimg/apple.PNG")
    apple_img = pygame.transform.scale(apple_img, (CELL_SIZE, CELL_SIZE))

start_img = None
exit_img = None

if os.path.exists("pythonimg/startbut.PNG"):
    start_img = pygame.image.load("pythonimg/startbut.PNG")
    start_img = pygame.transform.scale(start_img, (170, 65))
if os.path.exists("pythonimg/exitbut.PNG"):
    exit_img = pygame.image.load("pythonimg/exitbut.PNG")
    exit_img = pygame.transform.scale(exit_img, (150, 65))

score_file_path = "high_score.json"

def load_high_score():
    if os.path.exists(score_file_path):
        with open(score_file_path, "r") as f:
            data = json.load(f)
            return data.get("puls_game", 0)
    return 0

def save_high_score(new_score):
    data = {}
    if os.path.exists(score_file_path):
        with open(score_file_path, "r") as f:
            data = json.load(f)
    data["puls_game"] = new_score
    with open(score_file_path, "w") as f:
        json.dump(data, f, indent=4)

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


def main():
    board = [[random.randint(1, 9) for _ in range(cols)] for _ in range(rows)]
    score = 0
    start_time = time.time()
    selected_cells = []
    drag_start = None
    drag_end = None

    best_score = load_high_score()

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((255, 255, 255))
        elapsed = time.time() - start_time
        remaining_time = max(0, time_limit - int(elapsed))

        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, TOP_AREA))
        score_text = main_font.render("Score: " + str(score), True, (255, 0, 0))
        time_text = main_font.render("Time: " + str(remaining_time) + "s", True, (255, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (WIDTH - 150, 10))

        for i in range(rows):
            for j in range(cols):
                num = board[i][j]
                x = j * CELL_SIZE
                y = i * CELL_SIZE + TOP_AREA

                if num != 0:
                    if apple_img:
                        screen.blit(apple_img, (x, y))
                    text_surface = apple_font.render(str(num), True, (0, 0, 0))
                    text_x = x + CELL_SIZE // 2 - text_surface.get_width() // 2
                    text_y = y + CELL_SIZE // 2 - text_surface.get_height() //5
                    screen.blit(text_surface, (text_x, text_y))

                    if (i, j) in selected_cells:
                        shadow = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                        pygame.draw.ellipse(shadow, (0, 0, 0, 100), (0, 0, CELL_SIZE, CELL_SIZE))
                        screen.blit(shadow, (x, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= TOP_AREA:
                    col = x // CELL_SIZE
                    row = (y - TOP_AREA) // CELL_SIZE
                    drag_start = (row, col)
                    selected_cells = []

            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] == 1 and drag_start:
                    x, y = event.pos
                    if y >= TOP_AREA:
                        col = x // CELL_SIZE
                        row = (y - TOP_AREA) // CELL_SIZE
                        drag_end = (row, col)
                        selected_cells = []
                        r1, c1 = drag_start
                        r2, c2 = drag_end
                        for rr in range(min(r1, r2), max(r1, r2) + 1):
                            for cc in range(min(c1, c2), max(c1, c2) + 1):
                                selected_cells.append((rr, cc))

            elif event.type == pygame.MOUSEBUTTONUP:
                if drag_start and drag_end:
                    total = sum(board[r][c] for r, c in selected_cells)
                    if total == 10:
                        for r, c in selected_cells:
                            if board[r][c] != 0:
                                board[r][c] = 0
                        score += 10 
                    selected_cells = []
                    drag_start = None
                    drag_end = None

        pygame.display.flip()
        clock.tick(60)

        if remaining_time <= 0:
            running = False

    if score > best_score:
        save_high_score(score)
        best_score = score

    restart = show_game_over_screen(score, best_score)
    if restart:
        return main() 
    else:
        return False  

def start_puls_game():
    return main()

if __name__ == "__main__":
    start_puls_game()
