import pygame
import numpy as np
from math import *
from random import randint

pygame.init()

R = 255
G = 255
B = 255
RES = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
FPS = 30

scale = 100
circle_pos = [WIDTH/2, HEIGHT/2]  # x, y
angle_x = 0
angle_y = 0
angle_z = 0

# original points that make a cube
points = []
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))

# 2d projection matrix
projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

projected_points = [
    [n, n] for n in range(len(points))
]

def connect_points(i, j, points):
    pygame.draw.line(screen, pygame.Color('black'),
    (points[i][0], points[i][1]), (points[j][0], points[j][1]), width= 3)

def draw_polygon(color, points):
        pygame.draw.polygon(screen, pygame.Color(color), points)

run = True
clicking = False
while run:
    clock.tick(FPS)
    pygame.display.set_caption("3-D Cube")
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
                original_xpos = mx
                original_ypos = my
            if event.button == 4: #scrolling up: makes cube bigger
                scale += 5
            if event.button == 5: #scrolling down: makes cube smaller
                scale -= 5

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False

    # rotation matrices
    rotation_z = np.matrix([
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [-sin(angle_y), 0, cos(angle_y)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)],
    ])

    # calculates the distance of your current cursor position from where you originally clicked it
    if clicking:
        distance_x = abs(original_xpos - mx)
        distance_y = abs(original_ypos - my)

    if clicking and distance_x > WIDTH/30:
        if mx > original_xpos:
            angle_y += 0.0003 * distance_x
        if mx < original_xpos:
            angle_y -= 0.0003 * distance_x

    if clicking and distance_y > HEIGHT/30:
        if my > original_ypos:
            angle_x -= 0.0003 * distance_y
        if my < original_ypos:
            angle_x += 0.0003 * distance_y

    #automatically changes the z rotation if wanted
    angle_x += 0.01
    angle_y += 0.01
    angle_z += 0.01

    # changes the color of the background
    rand_num = randint(1,3)
    if rand_num == 1:
        if R < 255:
            R += 3
    if rand_num == 2:
        if G < 255:
            G += 3
    if rand_num == 3:
        if B < 255:
            B += 3
    if R == 255 and G == 255 and B == 255:
        R = 0
        G = 0
        B = 0

    screen.fill(pygame.Color(R,G,B))

    i = 0
    min_z = 0
    num_min_points = 0
    for point in points:
        rotated2d = np.dot(rotation_x, point.reshape(3,1))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_z, rotated2d)
        projected2d = np.dot(projection_matrix, rotated2d)

        if rotated2d[2] < min_z:
            min_z = rotated2d[2]
            excluded_point = i
        
        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]
        projected_points[i] = [x, y]
        pygame.draw.circle(screen, pygame.Color('black'), (x, y), 5 * (0.001 * scale))
        i += 1

    # checks if the "farthest back" point is not one of the points the shape is connecting to, and if it isnt, you draw the shape
    if excluded_point != 2 and excluded_point != 3 and excluded_point != 7 and excluded_point != 6:
        draw_polygon('purple', [projected_points[2],projected_points[3],projected_points[7],projected_points[6]])
    if excluded_point != 1 and excluded_point != 2 and excluded_point != 6 and excluded_point != 5:
        draw_polygon('orange', [projected_points[1],projected_points[2],projected_points[6],projected_points[5]])
    if excluded_point != 4 and excluded_point != 5 and excluded_point != 6 and excluded_point != 7:
        draw_polygon('green', projected_points[4:8])
    if excluded_point != 0 and excluded_point != 1 and excluded_point != 5 and excluded_point != 4:
        draw_polygon('yellow', [projected_points[0],projected_points[1],projected_points[5],projected_points[4]])
    if excluded_point != 0 and excluded_point != 4 and excluded_point != 7 and excluded_point != 3:
        draw_polygon('blue', [projected_points[0],projected_points[4],projected_points[7],projected_points[3]])
    if excluded_point != 0 and excluded_point != 1 and excluded_point != 2 and excluded_point != 3:
        draw_polygon('red', projected_points[0:4])

    if excluded_point != 0 and excluded_point != 1:
        connect_points(0, 1, projected_points)
    if excluded_point != 1 and excluded_point != 2:
        connect_points(1, 2, projected_points)
    if excluded_point != 2 and excluded_point != 3:
        connect_points(2, 3, projected_points)
    if excluded_point != 3 and excluded_point != 0:
        connect_points(3, 0, projected_points)
    if excluded_point != 4 and excluded_point != 5:
        connect_points(4, 5, projected_points)
    if excluded_point != 5 and excluded_point != 6:
        connect_points(5, 6, projected_points)
    if excluded_point != 6 and excluded_point != 7:
        connect_points(6, 7, projected_points)
    if excluded_point != 7 and excluded_point != 4:
        connect_points(7, 4, projected_points)
    if excluded_point != 0 and excluded_point != 4:
        connect_points(0, 4, projected_points)
    if excluded_point != 1 and excluded_point != 5:
        connect_points(1, 5, projected_points)
    if excluded_point != 2 and excluded_point != 6:
        connect_points(2, 6, projected_points)
    if excluded_point != 3 and excluded_point != 7:
        connect_points(3, 7, projected_points)

    pygame.display.update()