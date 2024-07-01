#               IMPORT LIBRARIES
import sys
import time
import os
import random

import pygame
from pygame import mixer

pygame.font.init()

mixer.init()

#               SETTING UP CONSTANTS
HEIGHT = 800
WIDTH = 1200
win = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 153)
ORANGE = (255, 165, 0)

COLOURS = [RED, GREEN, BLUE, WHITE]

CHAR_IMG = pygame.transform.scale_by(pygame.image.load(os.path.join("imgs", "mario.png")).convert(), 0.25)
CHAR_IMG.set_colorkey(WHITE)

ENEMY_IMG = pygame.transform.scale_by(pygame.image.load(os.path.join("imgs", "enemy.png")).convert(), 0.25)
ENEMY_IMG.set_colorkey(WHITE)
pygame.transform.flip(ENEMY_IMG, True, False)
ENEMY_NUM = 3
ENEMY_MIN_SPEED = 2
ENEMY_MAX_SPEED = 8

BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.jpeg")).convert(), (WIDTH, HEIGHT))
GND_IMG = pygame.image.load(os.path.join("imgs", "ground.png")).convert()

MENU_BTTN_SIZE = 60
MENU_BTTN = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "menu_bttn.png")).convert(),
                                   (MENU_BTTN_SIZE, MENU_BTTN_SIZE))
MENU_BTTN.set_colorkey(WHITE)

PLAY_BTTN = pygame.image.load(os.path.join("imgs", "play_bttn.png")).convert()
PLAY_BTTN.set_colorkey(WHITE)
PLAY_BTTN_X = WIDTH / 2 - PLAY_BTTN.get_width() / 2
PLAY_BTTN_Y = HEIGHT / 2 - PLAY_BTTN.get_height() / 2

PL_WIDTH = 300
PL_HEIGHT = 25
PL_NUM = 6
ZERO_HEIGHT = HEIGHT - GND_IMG.get_height()

jump_sound = pygame.mixer.Sound(os.path.join("sounds", "jump.mp3"))
jump_sound.set_volume(0.15)
enemy_killed_sound = pygame.mixer.Sound(os.path.join("sounds", "enemy_killed.mp3"))
coin_collected_sound = pygame.mixer.Sound(os.path.join("sounds", "coin_collected.mp3"))
death_sound = pygame.mixer.Sound(os.path.join("sounds", "death.mp3"))

g = 2
JUMP_VEL = 20
DEATH_VEL = 0

END_GAME_FONT = pygame.font.SysFont("comicsans", 75)


#               PLAYER CLASS
class Player:
    def __init__(self):
        self.x = 0
        self.y = HEIGHT - GND_IMG.get_height() - CHAR_IMG.get_height()
        self.IMGS = []
        self.img = CHAR_IMG
        self.dir = None
        self.x_vel = 8
        self.y_vel = 0
        self.jumped = False
        self.y_gnd = HEIGHT - GND_IMG.get_height()
        self.collided = False
        self.won = False
        self.killed = False

    def jump(self, y_gnd):
        if self.y + CHAR_IMG.get_height() == y_gnd:
            self.jumped = True
            self.y_vel = JUMP_VEL
            jump_sound.play()

    def lost(self, DEATH_VEL):
        DEATH_VEL -= 4 * g
        self.y -= DEATH_VEL

    def won(self):
        pass

    def move(self, x_coords, y_coords, enemies, killed):
        # x-coord
        if self.x + self.img.get_width() > WIDTH:
            self.x = WIDTH - self.img.get_width()

        if self.x < 0:
            self.x = 0

        # y-coord
        self.y_gnd = HEIGHT - GND_IMG.get_height()

        for coords_ind in range(len(x_coords)):
            if (x_coords[coords_ind][0] - CHAR_IMG.get_height() <= self.x <= x_coords[coords_ind][1]) and (
                    self.y + CHAR_IMG.get_height() <= y_coords[coords_ind]):
                self.y_gnd = y_coords[coords_ind]

        if self.jumped:
            self.y_vel -= g
            if self.y_vel <= -70:
                self.y_vel = 0
                self.jumped = False

        if self.y < 0:
            self.y = 0

        self.y -= self.y_vel

        # CHECKING EXCEPTIONS
        if self.y > self.y_gnd - CHAR_IMG.get_height():
            self.y = self.y_gnd - CHAR_IMG.get_height()
            self.jumped = False

        for enemy in enemies:
            if (enemy.x - CHAR_IMG.get_width() <= self.x <= enemy.x + ENEMY_IMG.get_width()) and (
                    self.y < enemy.y - CHAR_IMG.get_height()) and (
                    self.y - self.y_vel >= enemy.y - CHAR_IMG.get_height()):
                enemy.killed = True
                self.jump(self.y_gnd)

#CkinG_0-J06

            # enemy collision
            if not enemy.killed:
                if (enemy.x - CHAR_IMG.get_width() <= self.x <= enemy.x + ENEMY_IMG.get_width()) and (
                        enemy.y - CHAR_IMG.get_height() < self.y <= enemy.y + ENEMY_IMG.get_height()):
                    self.collided = True
                    death_sound.play()

            else:
                self.collided = False


#               ENEMY CLASS
class Enemy:
    def __init__(self, x, beg_x, end_x, y, speed):
        self.speed = speed
        self.BEG_X = beg_x
        self.END_X = end_x
        self.x = x
        self.y = y
        self.turn = True
        self.img = ENEMY_IMG
        self.IMGS = []
        self.killed = False

    def move(self):
        # x-coord
        if self.x + self.img.get_width() > WIDTH:
            self.x = WIDTH - self.img.get_width()
            self.turn = False
            self.speed = -self.speed

        if self.x + self.img.get_width() > self.END_X:
            self.x = self.END_X - ENEMY_IMG.get_width()
            self.turn = False
            self.speed = -self.speed

        if self.x < 0:
            self.x = 0
            self.turn = True
            self.speed = -self.speed

        if self.x < self.BEG_X:
            self.x = self.BEG_X
            self.turn = True
            self.speed = -self.speed

        self.x += self.speed


#               PLATFORM CLASS
class Platform:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.width = PL_WIDTH
        self.height = PL_HEIGHT
        self.surf_x_beg = self.x
        self.surf_x_end = self.x + self.width
        self.surf_y = y


#                   OTHER FUNCTIONS
#           "draw_game_display" FUNCTION UPDATES THE SCREEN EVERY TICK
def draw_game_display(platforms, char, turn_left, menu_pressed, enemies, x_coords, y_coords):
    win.blit(BG_IMG, (0, 0))

    win.blit(GND_IMG, (0, HEIGHT - GND_IMG.get_height()))
    win.blit(GND_IMG, (GND_IMG.get_width(), HEIGHT - GND_IMG.get_height()))
    win.blit(GND_IMG, (GND_IMG.get_width() * 2, HEIGHT - GND_IMG.get_height()))
    win.blit(GND_IMG, (GND_IMG.get_width() * 3, HEIGHT - GND_IMG.get_height()))

    for platform in platforms:
        pygame.draw.rect(win, platform.colour, pygame.Rect(platform.x, platform.y, platform.width, platform.height))

    if turn_left:
        win.blit(pygame.transform.flip(CHAR_IMG, True, False), (char.x, char.y))
    else:
        win.blit(CHAR_IMG, (char.x, char.y))

    win.blit(MENU_BTTN, (WIDTH - MENU_BTTN_SIZE, 0))

    for enemy in enemies:
        if not enemy.killed:
            if enemy.turn:
                win.blit(pygame.transform.flip(ENEMY_IMG, True, False), (enemy.x, enemy.y))
            else:
                win.blit(ENEMY_IMG, (enemy.x, enemy.y))

        else:
            char.jump(char.y + CHAR_IMG.get_height() + ENEMY_IMG.get_height())
            enemy_killed_sound.play()
            enemies.remove(enemy)

    if menu_pressed:
        win.blit(surface, (0, 0))
        pygame.draw.rect(surface, (0, 0, 0, 120), [0, 0, WIDTH, HEIGHT])
        win.blit(PLAY_BTTN, (PLAY_BTTN_X, PLAY_BTTN_Y))

    if char.collided:
        text = END_GAME_FONT.render("You have died, want to replay?", 1, WHITE)
        win.blit(text, (WIDTH / 15, HEIGHT / 2 - 40))

    if char.won:
        win.blit(surface, (0, 0))
        pygame.draw.rect(surface, (255, 255, 255, 180), [0, 0, WIDTH, HEIGHT])
        text1 = END_GAME_FONT.render("You have killed all the ghosts,", 1, ORANGE)
        text2 = END_GAME_FONT.render("CONGRATULATIONS!!!", 1, ORANGE)
        win.blit(text1, (WIDTH / 30, HEIGHT / 2 - 120))
        win.blit(text2, (WIDTH / 10, HEIGHT / 2))

    pygame.display.update()


#               "game" FUNCTION SETS THE ALGORITHM OF GAME
def game():
    #       BOOL VALUES
    turn_left = False
    menu_pressed = False

    #       SETTING UP A LIST OF COORDINATES FOR PLATFORMS
    plat_x_coords = []
    plat_y_coords = [ZERO_HEIGHT - 75, ZERO_HEIGHT - 150, ZERO_HEIGHT - 225, ZERO_HEIGHT - 300, ZERO_HEIGHT - 375,
                     ZERO_HEIGHT - 450]

    pl_x = random.randrange(WIDTH - PL_WIDTH)
    plat_x_coords.append(pl_x)

    for i in range(PL_NUM - 1):
        pl_x = random.randrange(WIDTH - PL_WIDTH)

        far_x = True
        while far_x:  # CHECKING THAT THE NEXT IS NOT TOO FAR FROM THE LAST ADDED ONE
            pl_x = random.randrange(WIDTH - PL_WIDTH)
            if PL_WIDTH < abs(pl_x - plat_x_coords[len(plat_x_coords) - 1]) < 400:
                far_x = False

            else:
                far_x = True

        plat_x_coords.append(pl_x)

    #       CREATING AND FILLING THE LIST OF PLATFORMS
    platforms = []

    for coord_ind in range(len(plat_x_coords)):
        colour_ind = random.randrange(len(COLOURS))
        platforms.append(Platform(plat_x_coords[coord_ind], plat_y_coords[coord_ind], COLOURS[colour_ind]))

    #       CREATING THE PLAYER'S CHARACTER
    character = Player()

    #       CREATING AND FILLING THE LISTS OF COORDINATES TO SPAWN ENEMIES
    x_coords = []
    y_coords = []

    for platform in platforms:
        x_coords.append([platform.surf_x_beg, platform.surf_x_end])
        y_coords.append(platform.surf_y)

    coord_indxs_for_enemies = []
    enemies = []

    #       SPAWNING ENEMIES ON RANDOM PLACE ON PLATFORM
    for _ in range(ENEMY_NUM):
        dome_ind = random.randrange(len(x_coords))
        while dome_ind in coord_indxs_for_enemies:
            dome_ind = random.randrange(len(x_coords))
        coord_indxs_for_enemies.append(dome_ind)
        beg_x = x_coords[dome_ind][0]
        end_x = x_coords[dome_ind][1]
        y = y_coords[dome_ind]
        x = random.randrange(end_x - beg_x) + beg_x
        speed = random.randrange(ENEMY_MAX_SPEED - ENEMY_MIN_SPEED) + ENEMY_MIN_SPEED

        enemy = Enemy(x, beg_x, end_x, y - ENEMY_IMG.get_height(), speed)
        enemies.append(enemy)

    #       LAUNCHING THE GAME LOOP
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)

        #       CHECKING ENDGAME SITUATIONS
        #           CHECKING ENDGAME SITUATION (WIN: ALL ENEMIES ARE ELIMINATED)
        if not enemies:
            character.won = True

        #           CHECKING ENDGAME SITUATION (WIN: ALL ENEMIES ARE ELIMINATED)
        if character.collided:
            character.lost(DEATH_VEL)
            draw_game_display(platforms, character, turn_left, menu_pressed, enemies, x_coords, y_coords)

        #       PROCESSING THE EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if (not character.collided) and (not character.won):
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                        character.jump(character.y_gnd)

                #       BUTTONS THAT CAN BE USED WHEN PLAYER LOST
                if character.collided:
                    if event.key == pygame.K_y:
                        game()

                    elif event.key == pygame.K_n:
                        sys.exit()

                #       BUTTONS THAT CAN BE USED WHEN PLAYER WON
                if character.won:
                    if event.key == pygame.K_y:
                        game()

                    elif event.key == pygame.K_n:
                        sys.exit()

                #       BUTTONS THAT CAN BE USED WHEN PLAYER IN MENU
                if event.key == pygame.K_ESCAPE:
                    if not character.won and not character.collided:
                        if not menu_pressed:
                            menu_pressed = True

                        else:
                            menu_pressed = False

            if event.type == pygame.MOUSEBUTTONUP:

                #       PLAYER IS ABLE TO USE MOUSE BUTTONS ONLY WHEN HE IS ALIVE (temporarily)
                if not character.won and not character.collided:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if menu_pressed:
                        if (PLAY_BTTN_X < mouse_x < PLAY_BTTN_X + PLAY_BTTN.get_width()) and (
                                PLAY_BTTN_Y < mouse_y < PLAY_BTTN_Y + PLAY_BTTN.get_height()):
                            menu_pressed = False
                    else:
                        if (WIDTH - MENU_BTTN_SIZE < mouse_x < WIDTH) and (0 < mouse_y < MENU_BTTN_SIZE):
                            menu_pressed = True

        #       PLAYER'S MOVEMENT PROCESSING
        if not character.collided:
            if (not menu_pressed) and (not character.won):
                if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                    character.x -= character.x_vel
                    turn_left = True

                if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                    character.x += character.x_vel
                    turn_left = False

                for enemy in enemies:
                    enemy.move()

            character.move(x_coords, y_coords, enemies, enemies)
            draw_game_display(platforms, character, turn_left, menu_pressed, enemies, x_coords, y_coords)


#               MAIN
game()
