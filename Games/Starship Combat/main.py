import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 600
BRD_WIDTH = 10
BRD_HEIGHT = HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blastar2")

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Gun+Silencer.mp3'))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
FPS = 60
VEL = 5
BUL_VEL = 10
MAX_BULS = 3

BORDER = pygame.Rect(WIDTH / 2 - BRD_WIDTH / 2, 0, BRD_WIDTH, BRD_HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMG = pygame.image.load(os.path.join(
    'Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMG = pygame.image.load(os.path.join(
    'Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

red = pygame.Rect(700, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
yellow = pygame.Rect(200, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH // 4 * 3 - red_health_text.get_width() // 2, 15))
    WIN.blit(yellow_health_text, (WIDTH // 4 - red_health_text.get_width() // 2, 15))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def movement(keys_pressed, player):
    if player == yellow:
        if keys_pressed[pygame.K_a] and player.x >= 0:  # Left
            player.x -= VEL
        if keys_pressed[pygame.K_d] and player.x <= BORDER.x - player.width:  # Right
            player.x += VEL
        if keys_pressed[pygame.K_w] and player.y >= 10:  # Up
            player.y -= VEL
        if keys_pressed[pygame.K_s] and player.y <= HEIGHT - player.height - 25:  # Down
            player.y += VEL

    if player == red:
        if keys_pressed[pygame.K_LEFT] and player.x >= BORDER.x + BORDER.width + 10:  # Left
            player.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and player.x <= WIDTH - player.width:  # Right
            player.x += VEL
        if keys_pressed[pygame.K_UP] and player.y >= 10:  # Up
            player.y -= VEL
        if keys_pressed[pygame.K_DOWN] and player.y <= HEIGHT - player.height - 25:  # Down
            player.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BUL_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BUL_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height / 2 - 2, 10, 4)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULS:
                    bullet = pygame.Rect(red.x, red.y + red.height / 2 - 2, 10, 4)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        keys_pressed = pygame.key.get_pressed()
        movement(keys_pressed, yellow)
        movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red wins"

        if winner_text != "":
            draw_winner(winner_text)
            break

    main()

if __name__ == "__main__":
    main()