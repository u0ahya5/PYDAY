# 파일 경로: python_project/screens/puls_Card.py

import pygame
import random
import time

# ────────────────────────────────────────────────────────────────────────
# 1) 게임 초기화 및 화면 설정 부분 (init_puls_game 함수로 분리)
def init_puls_game():
    """
    Puls 카드 게임을 초기화하고 필요한 변수들을 반환합니다.
    원래 사과 게임이었지만, 이 파일에서는 그대로 "Puls 카드 게임"으로 사용합니다.
    """
    pygame.init()
    
    # ① 화면 크기 변수 정의
    scr_width = 600
    scr_height = 700
    scr = pygame.display.set_mode((scr_width, scr_height))
    pygame.display.set_caption("Puls Card Game")
    
    # ② 폰트 설정
    fnt = pygame.font.Font(None, 30)
    big_fnt = pygame.font.Font(None, 50)

    # ③ 위쪽 정보 표시 영역 높이, 셀 크기, 행/열 개수, 시간 제한 등
    top_h = 50
    cell_sz = 45  # 셀 크기를 줄여서 여백 최소화
    c = scr_width // cell_sz
    r = (scr_height - top_h) // cell_sz
    t_lim = 120

    # ④ “사과 이미지” 대신, 이 자리에는 “Puls 카드 게임”에 필요한 이미지나 리소스를 불러와도 됩니다.
    #    여기서는 원본 코드를 유지하며, apple_img를 계속 사용해도 무방합니다.
    apple_img = pygame.image.load("pythonimg/apple.png")
    apple_img = pygame.transform.scale(apple_img, (cell_sz, cell_sz))

    # ⑤ 랜덤 숫자 보드 생성 (원본 그대로 사용)
    brd = [[random.randint(1, 9) for _ in range(c)] for _ in range(r)]

    # ⑥ 초기화된 모든 값을 호출자에게 반환
    return scr, fnt, big_fnt, r, c, cell_sz, t_lim, brd, top_h, apple_img


# ────────────────────────────────────────────────────────────────────────
# 2) 실제 게임 루프 부분 (play_puls_game)
def play_puls_game(scr, fnt, big_fnt, r, c, cell_sz, t_lim, brd, top_h, apple_img):
    """
    실제 Puls 카드 게임 로직이 동작하는 함수입니다.
    여기서는 기존 사과 게임 코드처럼 “셀을 선택해서 합이 10이면 제거” 기능을 유지합니다.
    """
    sel_cells = []
    s_cell = None  # 드래그 시작 셀
    e_cell = None  # 드래그 끝나는 셀
    score = 0
    st_time = time.time()
    is_running = True

    # ── 보드 그리기(사과+숫자+그림자)
    def draw_brd():
        for i in range(r):
            for j in range(c):
                num = brd[i][j]
                x = j * cell_sz
                y = i * cell_sz + top_h

                if num != 0:
                    # 🍎 사과 이미지(원본 코드 재활용)
                    scr.blit(apple_img, (x, y))

                    # 숫자 그리기
                    txt = fnt.render(str(num), True, (0, 0, 0))
                    txt_x = x + (cell_sz // 2 - txt.get_width() // 2)
                    txt_y = y + (cell_sz // 2 - txt.get_height() // 2)
                    scr.blit(txt, (txt_x, txt_y))

                    # 선택된 영역에는 그림자 효과 그리기
                    if (i, j) in sel_cells:
                        shadow = pygame.Surface((cell_sz, cell_sz), pygame.SRCALPHA)
                        pygame.draw.ellipse(shadow, (0, 0, 0, 100), (0, 0, cell_sz, cell_sz))
                        scr.blit(shadow, (x, y))

    # ── 상단 점수/남은시간 표시
    def draw_top(remaining, score):
        pygame.draw.rect(scr, (255, 255, 255), (0, 0, c * cell_sz, top_h))
        score_txt = fnt.render(f"Score: {score}", True, (255, 0, 0))
        time_txt = fnt.render(f"Time: {remaining}s", True, (255, 0, 0))
        scr.blit(score_txt, (10, 10))
        scr.blit(time_txt, (c * cell_sz - 200, 10))

    # ── 셀 좌표 계산 (마우스 클릭 위치 → (row, col) 반환)
    def get_cell(pos):
        x, y = pos
        if y < top_h:
            return None
        col = x // cell_sz
        row = (y - top_h) // cell_sz
        if 0 <= row < r and 0 <= col < c:
            return (row, col)
        return None

    # ── 드래그로 선택된 영역 내 셀 좌표 모음
    def select_range(s, e):
        nonlocal sel_cells
        sel_cells = []
        if s and e:
            s_row, s_col = s
            e_row, e_col = e
            for i in range(min(s_row, e_row), max(s_row, e_row) + 1):
                for j in range(min(s_col, e_col), max(s_col, e_col) + 1):
                    sel_cells.append((i, j))

    # ── 선택된 셀들의 합
    def calc_sum():
        return sum(brd[i][j] for i, j in sel_cells)

    # ── 합이 10인 셀 제거하고 점수 올리기
    def remove_cells():
        nonlocal score
        for i, j in sel_cells:
            if brd[i][j] != 0:
                score += 1
                brd[i][j] = 0

    # ──────────────────────────────────────────────────────────────────
    # 메인 게임 루프
    while is_running:
        elapsed = time.time() - st_time
        remaining = max(0, t_lim - int(elapsed))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 드래그 시작: 시작 셀 저장, 이전 선택 초기화
                s_cell = get_cell(event.pos)
                sel_cells.clear()

            elif event.type == pygame.MOUSEBUTTONUP:
                # 드래그 끝: 끝 셀 저장 후 합 계산/삭제 기능
                e_cell = get_cell(event.pos)
                if s_cell and e_cell:
                    select_range(s_cell, e_cell)
                    if calc_sum() == 10:
                        remove_cells()
                s_cell = None  # 드래그 모드 해제

            elif event.type == pygame.MOUSEMOTION:
                # 마우스 이동 중: 좌클릭(버튼 0) 상태에서만 드래그 선택 갱신
                if event.buttons[0] == 1 and s_cell:
                    e_cell = get_cell(event.pos)
                    if e_cell:
                        select_range(s_cell, e_cell)

        # 시간 종료 시 루프 탈출
        if remaining == 0:
            is_running = False

        # 화면 그리기
        scr.fill((255, 255, 255))
        draw_top(remaining, score)
        draw_brd()
        pygame.display.flip()

    return score


# ────────────────────────────────────────────────────────────────────────
# 3) 게임 종료 화면 표시 함수 (show_end_puls)
def show_end_puls(scr, fin_score):
    scr.fill((255, 255, 255))
    big_fnt = pygame.font.Font(None, 50)
    txt = big_fnt.render(f"Game over! Your Score: {fin_score}", True, (0, 0, 0))
    scr.blit(
        txt,
        (
            scr.get_width() // 2 - txt.get_width() // 2,
            scr.get_height() // 2 - txt.get_height() // 2
        )
    )
    pygame.display.flip()
    pygame.time.wait(3000)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

    pygame.quit()


# ────────────────────────────────────────────────────────────────────────
# 4) 외부에서 호출할 진입점 함수 (start_puls_game)
def start_puls_game(screen):
    """
    main.py나 gamelist.py에서 이 함수를 호출하면,
    내부적으로 init → play → 종료화면 순서로 수행됩니다.
    """
    scr, fnt, big_fnt, r, c, cell_sz, t_lim, brd, top_h, apple_img = init_puls_game()
    final_score = play_puls_game(scr, fnt, big_fnt, r, c, cell_sz, t_lim, brd, top_h, apple_img)
    show_end_puls(scr, final_score)


# ────────────────────────────────────────────────────────────────────────
# 5) 단독 실행(테스트)용 블록
if __name__ == "__main__":
    pygame.init()
    scr, fnt, big_fnt, r, c, cell_sz, t_lim, brd, top_h, apple_img = init_puls_game()
    final_score = play_puls_game(scr, fnt, big_fnt, r, c, cell_sz, t_lim, brd, top_h, apple_img)
    show_end_puls(scr, final_score)
