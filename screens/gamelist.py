import pygame
from screens.puls_Card import start_puls_game
from screens.appletree_Card import start_appletree_game
from screens.avoid_Card import start_avoid_game

def show_game_select_screen(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    background_color = (247, 240, 232)
    
    # ── 1) 게임 이미지 로드 및 크기 조정
    puls_img = pygame.image.load("pythonimg/puls_card.png")
    puls_img = pygame.transform.scale(puls_img, (150, 150))
    
    apple_img = pygame.image.load("pythonimg/appletree_card.png")
    apple_img = pygame.transform.scale(apple_img, (150, 150))
    
    avoid_img = pygame.image.load("pythonimg/avoid_card.png")
    avoid_img = pygame.transform.scale(avoid_img, (150, 150))
    
    # ── 2) 이미지의 화면 내 위치 설정 (topleft)
    #     예: 화면 크기가 600×700이라고 가정할 때,
    #          위쪽에 제목 영역(높이 약 50)을 남겨두고,
    #          각 이미지를 가로 50px 간격으로 배치
    puls_rect = puls_img.get_rect(topleft=(50, 100))
    apple_rect = apple_img.get_rect(topleft=(225, 100))
    avoid_rect = avoid_img.get_rect(topleft=(400, 100))
    
    game_buttons = {
        "puls": (puls_img, puls_rect),
        "apple": (apple_img, apple_rect),
        "avoid": (avoid_img, avoid_rect),
    }
    
    # ── 3) “시작” 버튼 Rect 정의 (나중에 클릭 시 실제 게임 진입)
    start_button = pygame.Rect(225, 550, 150, 50)
    selected_game = None
    
    running = True
    while running:
        screen.fill(background_color)
        
        # 제목
        title = font.render("게임을 선택하세요", True, (0, 0, 0))
        screen.blit(title, (200, 30))
        
        # ── 4) 게임 이미지와 선택 테두리(그림자 등) 그리기
        for key, (img, rect) in game_buttons.items():
            screen.blit(img, rect)
            if selected_game == key:
                # 간단히 빨간 테두리
                pygame.draw.rect(screen, (255, 0, 0), rect, 4)
        
        # ── 5) 선택된 항목이 있으면, Start 버튼도 같이 그리기
        if selected_game is not None:
            pygame.draw.rect(screen, (0, 120, 0), start_button)
            btn_text = font.render("게임 시작", True, (255, 255, 255))
            screen.blit(btn_text, (start_button.x + 20, start_button.y + 10))
        
        pygame.display.flip()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1) 게임 카드 클릭: selected_game 값 갱신
                for key, (_, rect) in game_buttons.items():
                    if rect.collidepoint(event.pos):
                        selected_game = key if selected_game != key else None
                        break
                
                # 2) Start 버튼 클릭: 실제 게임 함수 호출
                if selected_game and start_button.collidepoint(event.pos):
                    if selected_game == "puls":
                        print(">> Puls 카드 선택, 이제 start_puls_game 호출")  # 디버그용
                        start_puls_game(screen)
                    elif selected_game == "apple":
                        print(">> Apple 카드 선택, 이제 start_appletree_game 호출")  # 디버그용
                        start_appletree_game(screen)
                    elif selected_game == "avoid":
                        print(">> Avoid 카드 선택, 이제 start_avoid_game 호출")  # 디버그용
                        start_avoid_game(screen)
                    running = False
