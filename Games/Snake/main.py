import random
import pygame
import os
import time
pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 800

VEL = 20
K_PIXEL = 20

BLACK = (0, 0, 0)
STAT_FONT = pygame.font.SysFont("comicsans", 25)

HEAD_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "snake_head.png")), (20, 20))
BODY_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "snake_body.png")), (20, 20))
APPLE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "apple.png")), (20, 20))

class Head(object):
    IMG = HEAD_IMG

    def __init__(self):
        self.dir = "right"
        self.vel = VEL
        self.x = WIN_WIDTH / 2
        self.y = WIN_HEIGHT / 2

    def turn_up(self):
        self.dir = "up"

    def turn_down(self):
        self.dir = "down"

    def turn_left(self):
        self.dir = "left"

    def turn_right(self):
        self.dir = "right"


    def move(self):
        if self.dir == "up":
            self.y -= self.vel

        elif self.dir == "down":
            self.y += self.vel

        elif self.dir == "left":
            self.x -= self.vel

        elif self.dir == "right":
            self.x += self.vel

        if self.x + self.IMG.get_width() > WIN_WIDTH:
            self.x = 0

        if self.x < 0:
            self.x = WIN_WIDTH - self.IMG.get_width()

        if self.y + self.IMG.get_height() > WIN_HEIGHT:
            self.y = 0

        if self.y < 0:
            self.y = WIN_HEIGHT - self.IMG.get_height()

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

class Body(object):
    IMG = BODY_IMG

    def __init__(self, x, y, tick, b_dir):
        self.x = x
        self.y = y
        self.tick = tick
        self.dir = b_dir
        self.vel = VEL
        self.index = 0

    def move(self):
        if self.dir == "up":
            self.y -= self.vel

        elif self.dir == "down":
            self.y += self.vel

        elif self.dir == "left":
            self.x -= self.vel

        elif self.dir == "right":
            self.x += self.vel

        if self.x + self.IMG.get_width() > WIN_WIDTH:
            self.x = 0

        if self.x < 0:
            self.x = WIN_WIDTH - self.IMG.get_width()

        if self.y + self.IMG.get_height() > WIN_HEIGHT:
            self.y = 0

        if self.y < 0:
            self.y = WIN_HEIGHT - self.IMG.get_height()

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


class Apple(object):
    IMG = APPLE_IMG

    def __init__(self):
        self.x = random.randrange((WIN_WIDTH - self.IMG.get_width()) // K_PIXEL) * K_PIXEL
        self.y = random.randrange((WIN_HEIGHT - self.IMG.get_height()) // K_PIXEL) * K_PIXEL

    def draw(self, win, snake_x, snake_y, snake, tick, score, body):
        win.blit(self.IMG, (self.x, self.y))

    def is_collected(self, x, y):
        if (x == self.x) and (y == self.y):
            return True
        else:
            return False


def add_body(body, x, y, tick, direction):
    if direction == "up":
        body.append(Body(x, y + K_PIXEL, tick, direction))

    if direction == "down":
        body.append(Body(x, y - K_PIXEL, tick, direction))

    if direction == "left":
        body.append(Body(x + K_PIXEL, y, tick, direction))

    if direction == "right":
        body.append(Body(x - K_PIXEL, y, tick, direction))


def check_and_change_dir(old_directions, old_coordinates, body, DIR):
    # Delete the first coordinate when the last body block crossed it
    #if len(body) > 1:
    # Change the direction of movement of body block if its coordinate is the same as any from list
    for b in body:
        coordinate = [b.x, b.y]
        if b.index > len(old_coordinates) - 1:  # if index goes beyond the range of coord list
            if coordinate == old_coordinates[len(old_coordinates) - 1]:  # if the coordinate index in the list is the last one
                b.dir = DIR
        else:  # if index does not go beyond the range of coord list
            if coordinate == old_coordinates[b.index]:
                if len(old_directions) < b.index + 1:
                    b.dir = DIR

                else:
                    b.dir = old_directions[b.index + 1]

    #else:
  #      if old_coordinates:
  #          if [body[0].x, body[0].y] == old_coordinates[0]:
  #              body[0].dir = DIR
   #     else:
   #         body[0].dir = DIR
def draw_window(win, snake, apple, body, tick, score):
    win.fill(BLACK)
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    for b in body:
        b.draw(win)
    apple.draw(win, snake.x, snake.y, snake, tick, score, body)
    snake.draw(win)

    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    snake = Head()
    apple = Apple()
    body = []
    old_coordinates = []
    old_directions = []
    score = 0
    tick = 5
    run = True

    while run:
        clock.tick(tick)
        snake.draw(win)
        old_direction = snake.dir
        old_coordinate = [snake.x, snake.y]
        diff = 1


        if apple.is_collected(snake.x, snake.y):
            score += 1
            tick += 0.5
            apple.x = random.randrange((WIN_WIDTH - apple.IMG.get_width()) // K_PIXEL) * K_PIXEL
            apple.y = random.randrange((WIN_HEIGHT - apple.IMG.get_height()) // K_PIXEL) * K_PIXEL

            for b in body:
                b.index += 1

            if body:
                add_body(body, body[len(body) - 1].x, body[len(body) - 1].y, tick, body[len(body) - 1].dir)
            else:
                add_body(body, snake.x, snake.y, tick, snake.dir)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                print(old_directions)
                print(old_coordinates)
                if event.key == pygame.K_UP:
                    if snake.dir != "down":
                        old_coordinates.append(old_coordinate)
                        old_directions.append(old_direction)

                        if len(body) + 1 < len(old_directions):
                            print("Deleted")
                            old_coordinates = old_coordinates[diff:]
                            old_directions = old_directions[diff:]

                        snake.turn_up()

                if event.key == pygame.K_DOWN:
                    if snake.dir != "up":
                        old_coordinates.append(old_coordinate)
                        old_directions.append(old_direction)

                        if len(body) + 1 < len(old_directions):
                            print("Deleted")
                            old_coordinates = old_coordinates[diff:]
                            old_directions = old_directions[diff:]

                        snake.turn_down()

                if event.key == pygame.K_LEFT:
                    if snake.dir != "right":
                        old_coordinates.append(old_coordinate)
                        old_directions.append(old_direction)

                        if len(body) + 1 < len(old_directions):
                            print("Deleted")
                            old_coordinates = old_coordinates[diff:]
                            old_directions = old_directions[diff:]

                        snake.turn_left()

                if event.key == pygame.K_RIGHT:
                    if snake.dir != "left":
                        old_coordinates.append(old_coordinate)
                        old_directions.append(old_direction)

                        if len(body) + 1 < len(old_directions):
                            print("Deleted")
                            old_coordinates = old_coordinates[diff:]
                            old_directions = old_directions[diff:]

                        snake.turn_right()

        if body:
            check_and_change_dir(old_directions, old_coordinates,
                                 body, snake.dir)

        snake.move()
        for b in body:
            b.move()

        draw_window(win, snake, apple, body, tick, score)

    pygame.quit()
    quit()

main()