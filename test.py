import pygame
import random
import time


# 게임 초기화 및 화면 설정
def init_game():
    pygame.init()
    scr_width = 600
    scr_height = 700
    scr = pygame.display.set_mode((scr_width, scr_height))
    pygame.display.set_caption("Apple Game")
    fnt = pygame.font.Font(None, 30)
    big_fnt = pygame.font.Font(None, 50)

    # 화면에 맞게 셀 수와 크기 조정
    top_h = 50
    cell_sz = 50
    c = scr_width // cell_sz  # 600 / 50 = 12
    r = (scr_height - top_h) // cell_sz  # (700 - 50) / 50 = 13
    t_lim = 120
    return scr, fnt, big_fnt, r, c, cell_sz, t_lim


def make_board(r, c):
    return [[random.randint(1, 9) for _ in range(c)] for _ in range(r)]


# 게임 실행
def play_game(scr, fnt, big_fnt, r, c, cell_sz, t_lim):
    brd = make_board(r, c)
    sel_cells = []
    s_cell = None
    e_cell = None
    score = 0
    st_time = time.time()
    top_h = 50
    is_running = True

    # 게임 보드 그리기
    def draw_brd():
        for i in range(r):
            for j in range(c):
                num = brd[i][j]
                if num != 0:
                    txt = fnt.render(str(num), True, (0, 0, 0))
                    x = j * cell_sz + (cell_sz // 2 - txt.get_width() // 2)
                    y = i * cell_sz + top_h + (cell_sz // 2 - txt.get_height() // 2)
                    if (i, j) in sel_cells:
                        pygame.draw.rect(scr, (255, 0, 0), (j * cell_sz, i * cell_sz + top_h, cell_sz, cell_sz))
                    scr.blit(txt, (x, y))

    # 점수/남은시간 표시
    def draw_top(remaining, score):
        pygame.draw.rect(scr, (255, 255, 255), (0, 0, c * cell_sz, top_h))
        score_txt = fnt.render(f"Score: {score}", True, (255, 0, 0))
        time_txt = fnt.render(f"Time: {remaining}s", True, (255, 0, 0))
        scr.blit(score_txt, (10, 10))
        scr.blit(time_txt, (c * cell_sz - 200, 10))

    # 클릭 위치 좌표 찾기
    def get_cell(pos):
        x, y = pos
        if y < top_h:
            return None
        col = x // cell_sz
        row = (y - top_h) // cell_sz
        if 0 <= row < r and 0 <= col < c:
            return (row, col)
        return None

    # 선택된 범위의 셀 저장
    def select_range(s, e):
        nonlocal sel_cells
        sel_cells = []
        if s and e:
            s_row, s_col = s
            e_row, e_col = e
            for i in range(min(s_row, e_row), max(s_row, e_row) + 1):
                for j in range(min(s_col, e_col), max(s_col, e_col) + 1):
                    sel_cells.append((i, j))

    def calc_sum():
        return sum(brd[i][j] for i, j in sel_cells)

    # 선택된 셀 제거(점수 증가)
    def remove_cells():
        nonlocal score
        for i, j in sel_cells:
            if brd[i][j] != 0:
                score += 1
                brd[i][j] = 0

    while is_running:
        elapsed = time.time() - st_time
        remaining = max(0, t_lim - int(elapsed))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                s_cell = get_cell(event.pos)
                sel_cells.clear()
            elif event.type == pygame.MOUSEBUTTONUP:
                e_cell = get_cell(event.pos)
                if s_cell and e_cell:
                    select_range(s_cell, e_cell)
                    if calc_sum() == 10:
                        remove_cells()
            elif event.type == pygame.MOUSEMOTION and s_cell:
                e_cell = get_cell(event.pos)
                select_range(s_cell, e_cell)

        if remaining == 0:
            is_running = False

        scr.fill((255, 255, 255))
        draw_top(remaining, score)
        draw_brd()
        pygame.display.flip()

    return score


# 게임 종료 화면 표시
def show_end(scr, fin_score):
    scr.fill((255, 255, 255))
    big_fnt = pygame.font.Font(None, 50)
    txt = big_fnt.render(f"Game over! Your Score: {fin_score}", True, (0, 0, 0))
    scr.blit(txt, (scr.get_width() // 2 - txt.get_width() // 2, scr.get_height() // 2 - 100))
    pygame.display.flip()
    pygame.time.wait(3000)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

    pygame.quit()


# 메인 함수 실행
if __name__ == "__main__":
    scr, fnt, big_fnt, r, c, cell_sz, t_lim = init_game()
    final_score = play_game(scr, fnt, big_fnt, r, c, cell_sz, t_lim)
    show_end(scr, final_score)