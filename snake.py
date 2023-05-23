import pygame as pg 
from random import randrange

WINDOW = 1000
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE -2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0,0)
time, time_step = 0, 110
food = snake.copy()
food.center = get_random_position()
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1, pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1} # this defines where it is acceptible to move. Then, we can use this later to define what is unacceptible. Specifically, moving backwards or "into itself". 

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w or event.key == pg.K_UP:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1, pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if event.key == pg.K_s or event.key == pg.K_DOWN:
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1, pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                snake_dir = (-TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0, pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1, pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}
    screen.fill('black')
    # Check borders - make sure the player stays in bounds or else the game ends! Also, add something to prevent self-easting.
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]
    # Create the interaction between the snake and the food. The snake should get bigger, and the food should change location.
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1
    # Draw food
    pg.draw.rect(screen, "cyan", food)
    # Draw snake below
    [pg.draw.rect(screen, 'magenta', segment) for segment in segments]
    # Move snake and its segments. Then, control the speed by using timestep.
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now 
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
    pg.display.flip()
    clock.tick(60)