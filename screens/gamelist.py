import pygame
from screens.puls_Card import start_puls_game
from screens.appleclick_Card import start_appleclick_game
from screens.avoid_Card import start_avoid_game

def show_game_select_screen(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  
    background_color = (247, 240, 232)

    puls_img = pygame.image.load("pythonimg/puls_Card.png").convert_alpha()
    puls_img = pygame.transform.scale(puls_img, (150, 150))

    apple_img = pygame.image.load("pythonimg/appleclick_Card.png").convert_alpha()
    apple_img = pygame.transform.scale(apple_img, (150, 150))

    avoid_img = pygame.image.load("pythonimg/avoid_card.png").convert_alpha()
    avoid_img = pygame.transform.scale(avoid_img, (150, 150))

    # Start 버튼 이미지 로드
    start_img = pygame.image.load("pythonimg/startbut.png").convert_alpha()
    start_img = pygame.transform.scale(start_img, (150, 65))

    # 카드 위치
    puls_rect = puls_img.get_rect(topleft=(20, 200))
    apple_rect = apple_img.get_rect(topleft=(180, 200))
    avoid_rect = avoid_img.get_rect(topleft=(340, 200))

    # Start 버튼 위치
    center_x = screen.get_width() // 2
    start_rect = start_img.get_rect(center=(center_x, 500))

    game_buttons = {
        "puls": (puls_img, puls_rect),
        "apple": (apple_img, apple_rect),
        "avoid": (avoid_img, avoid_rect),
    }

    selected_game = None
    running = True

    while running:
        screen.fill(background_color)

        # 제목
        title = font.render("PYDAY", True, (255, 187, 0))
        screen.blit(title, (215, 30))

        for key, (img, rect) in game_buttons.items():
            screen.blit(img, rect)
            if selected_game == key:
                pygame.draw.rect(screen, (255, 197, 72), rect, width=5, border_radius=5)

        if selected_game is not None:
            screen.blit(start_img, start_rect)

        pygame.display.flip()
        clock.tick(60)

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False

            elif evt.type == pygame.MOUSEBUTTONDOWN:
                # 카드 클릭 → 선택 토글
                for key, (_, rect) in game_buttons.items():
                    if rect.collidepoint(evt.pos):
                        selected_game = key if selected_game != key else None
                        break

                # Start 버튼 클릭 → 게임 실행
                if selected_game and start_rect.collidepoint(evt.pos):
                    if selected_game == "puls":
                        if start_puls_game() is False:
                            show_game_select_screen(screen)
                    elif selected_game == "apple":
                        if start_appleclick_game(screen) is False:
                            show_game_select_screen(screen)
                    elif selected_game == "avoid":
                        if start_avoid_game() is False:
                            show_game_select_screen(screen)
                    running = False
