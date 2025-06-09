import pygame
import random

# 게임 설정
WIDTH, HEIGHT = 600, 700
FPS = 60

# 색 정의 (필요 시)
WHITE = (255, 255, 255)

# 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("폭탄 피하기")
clock = pygame.time.Clock()

# 이미지 로드
background = pygame.image.load("pythonimg/avoid_bg.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player_img = pygame.image.load("pie.png").convert_alpha()
player_rect = player_img.get_rect()
sun_img = pygame.image.load("sun.png").convert_alpha()
poison_img = pygame.image.load("poison_apple.png").convert_alpha()

# 플레이어 초기 위치
player_rect.centerx = WIDTH // 2
player_rect.bottom = HEIGHT - 10
PLAYER_SPEED = 5

# 아이템 그룹
suns = []  # 해 모양 아이템 리스트
poisons = []  # 폭탄 리스트

# 점수
score = 0
font = pygame.font.SysFont(None, 36)

def spawn_sun():
    x = random.randint(0, WIDTH - sun_img.get_width())
    y = -sun_img.get_height()
    suns.append(pygame.Rect(x, y, sun_img.get_width(), sun_img.get_height()))


def spawn_poison():
    x = random.randint(0, WIDTH - poison_img.get_width())
    y = -poison_img.get_height()
    poisons.append(pygame.Rect(x, y, poison_img.get_width(), poison_img.get_height()))

running = True
spawn_timer = 0
spawn_interval = 30  # 프레임 단위

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += PLAYER_SPEED

    # 아이템 스폰
    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        spawn_timer = 0
        if random.random() < 0.7:
            spawn_poison()
        else:
            spawn_sun()

    # 아이템 이동
    for rect in suns[:]:
        rect.y += 4
        if rect.top > HEIGHT:
            suns.remove(rect)
        elif rect.colliderect(player_rect):
            score += 10
            suns.remove(rect)

    for rect in poisons[:]:
        rect.y += 6
        if rect.top > HEIGHT:
            poisons.remove(rect)
        elif rect.colliderect(player_rect):
            running = False  # 게임 오버

    # 랜더링
    screen.blit(background, (0, 0))
    screen.blit(player_img, player_rect)
    for rect in suns:
        screen.blit(sun_img, rect)
    for rect in poisons:
        screen.blit(poison_img, rect)

    # 점수 표시
    score_surf = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surf, (10, 10))

    pygame.display.flip()

pygame.quit()
