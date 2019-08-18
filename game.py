import pygame
import random
import sys
from time import sleep

BLACK = (0, 0, 0)
RED = (255, 0, 0)
pad_width = 800
pad_height = 700
fighter_width = 80
fighter_height = 80
enemy_width = 70
enemy_height = 70
background_height = 640


def back( x, y):
    global gamepad, background
    gamepad.blit(background, (x, y))


def draw_score(count):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render('Score: ' + str(count * 100), True, (255, 255, 255))
    gamepad.blit(text, (0, 0))


def draw_passed(count):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render('Left Life: ' + str(3 - count), True, (255, 255, 255))
    gamepad.blit(text, (720, 0))


def disp_message(text):
    global gamepad
    textfont = pygame.font.Font('freesansbold.ttf', 80)
    text = textfont.render(text, True, (255, 255, 000))
    textpos = text.get_rect()
    textpos.center = (pad_width / 2, pad_height / 2)
    gamepad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    run_game()


def crash():
    global gamepad
    disp_message('Crashed!')


def gameover():
    global gamepad
    disp_message('Game Over')


def draw_object(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))


def run_game():
    global gamepad, clock, fighter, enemy, bullet, background, boom

    isShot = False
    shotcount = 0
    enemypassed = 0
    boomcount = 0

    bullet_xy = []

    x = pad_width * 0.45
    y = pad_height * 0.8
    x_change = 0

    enemy_x = random.randrange(0, pad_width - enemy_width)
    enemy_y = 0
    enemy_speed = 1

    ongame = False
    while not ongame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change -= 15

                elif event.key == pygame.K_RIGHT:
                    x_change += 15

                elif event.key == pygame.K_SPACE:
                    if len(bullet_xy) < 20:
                        bullet_x = x + fighter_width / 2
                        bullet_y = y - fighter_height / 4
                        bullet_xy.append([bullet_x, bullet_y])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        gamepad.fill(BLACK)
        back(0,0)

        x += x_change
        if x < 0:
            x = 0
        elif x > pad_width - fighter_width:
            x = pad_width - fighter_width

        if y < enemy_y + enemy_height:
            if (enemy_x > x and enemy_x < x + fighter_width) or \
                    (enemy_x + enemy_width > x and enemy_x + enemy_width < x + fighter_width):
                crash()
        draw_object(fighter, x, y)

        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[1] -= 10
                bullet_xy[i][1] = bxy[1]

                if bxy[1] < enemy_y:
                    if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_width:
                        bullet_xy.remove(bxy)
                        isShot = True
                        shotcount += 1
                    if bxy[1] <= 0:
                        try:
                            bullet_xy.remove(bxy)
                        except:
                            pass

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                draw_object(bullet, bx, by)

        draw_score(shotcount)

        enemy_y += enemy_speed

        if enemy_y > pad_height:
            enemy_y = 0
            enemy_x = random.randrange(0, pad_width - enemy_width)
            enemypassed += 1

        if enemypassed == 3:
            gameover()

        draw_passed(enemypassed)

        if isShot:
            draw_object(boom, enemy_x, enemy_y)
            boomcount += 1
            if boomcount > 5:
                enemy_x = random.randrange(0, pad_width - enemy_width)
                enemy_y = 0
                isShot = False
                boomcount = 0
                enemy_speed += 0.5
                if enemy_speed >= 10:
                    enemy_speed = 10
        else:
            draw_object(enemy, enemy_x, enemy_y)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()


def init_game():
    global gamepad, clock, fighter, enemy, bullet, background, boom

    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('Fight Bug (spoqa)')
    fighter = pygame.image.load('pyicon.png')
    enemy = pygame.image.load('bug.png')
    bullet = pygame.image.load('bullet.png')
    background = pygame.image.load('pythonistas.png')
    boom = pygame.image.load('boom.png')
    clock = pygame.time.Clock()


init_game()
run_game()
