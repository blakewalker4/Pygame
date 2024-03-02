import pygame
from random import randint
from copy import deepcopy
import time

pygame.init()
pygame.mixer.init()

RES = WIDTH, HEIGHT = 900, 900
TILE = 10
W, H = WIDTH // TILE, HEIGHT // TILE
FPS = 5

surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
# makes an empty array for the next frame
next_field = [[0 for i in range(W)] for j in range(H)]

# pre-set starting points for the game:

# current_field = [[0 for i in range(W)] for j in range(H)]
# current_field = [[1 if i == W // 2 or j == H // 2 else 0 for i in range(W)] for j in range(H)]
# current_field = [[randint(0, 1) for i in range(W)] for j in range(H)]
# current_field = [[1 if not i % 9 else 0 for i in range(W)] for j in range(H)] # 2,5,8,9,10,11,13,18,21,22,26,30,33,65
# current_field = [[1 if not (2 * i + j) % 4 else 0 for i in range(W)] for j in range(H)] # (2,4),(4,4)
current_field = [[1 if not (i * j) % 22 else 0 for i in range(W)] for j in range(H)] # 5,6,9,22,33
# current_field = [[1 if not i % 7 else randint(0, 1) for i in range(W)] for j in range(H)]
# current_field = [[1 if i == j or i == (W - j) else 0 for i in range(W)] for j in range(H)]

def check_cell(current_field, x, y):
    count = 0
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if current_field[j][i]:
                count += 1

    if current_field[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 3:
            return 1
        return 0

run, pause = True, True
left_clicking, right_clicking = False, False

while run:
    pause_start_time = time.time()
    clock.tick(FPS)
    pygame.display.set_caption("press space to pause. FPS: " + str(clock.get_fps()) + " Is playing: " + str(not(pause)))
    surface.fill(pygame.Color('black'))

    [pygame.draw.line(surface, pygame.Color('darkslategray'), (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, TILE)]
    [pygame.draw.line(surface, pygame.Color('darkslategray'), (0, y), (WIDTH, y)) for y in range(0, HEIGHT, TILE)]

    # clicking currently doesnt do anything
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if pause == False and event.key == pygame.K_SPACE:
                pause_start_time = time.time()
                pause = True
            if pause == True and event.key == pygame.K_SPACE and time.time() > pause_start_time + 0.1:
                pause = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_clicking = True
            if event.button == 3:
                right_clicking = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                left_clicking = False
            if event.button == 3:
                right_clicking = False
                
    
    # draw life
    if not(pause):
        for x in range(1, W - 1):
            for y in range(1, H - 1):
                if current_field[y][x]:
                    pygame.draw.rect(surface, pygame.Color('forestgreen'), (x * TILE + 0, y * TILE + 2, TILE - 2, TILE - 2))
                next_field[y][x] = check_cell(current_field, x, y)

        current_field = deepcopy(next_field)

        pygame.display.flip()
