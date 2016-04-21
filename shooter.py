import pygame
import gamebox
import random

# camera
camera = gamebox.Camera(800, 600)

# player ship
player = gamebox.from_color(400, 550, "red", 30, 30)

# default bullets
bullet1 = gamebox.from_color(-5, 520, "yellow", 5, 5)
bullet2 = gamebox.from_color(-5, 520, "yellow", 5, 5)
bullet3 = gamebox.from_color(-5, 520, "yellow", 5, 5)
bullets = [bullet1, bullet2, bullet3]

# enemies and their weapons
enemies = []
en_bullet1 = gamebox.from_color(-5, 520, "red", 5, 5)
en_bullet2 = gamebox.from_color(-5, 520, "red", 5, 5)
en_bullet3 = gamebox.from_color(-5, 520, "red", 5, 5)
en_bullets = [en_bullet1, en_bullet2, en_bullet3]


def create_enemy():
    enemy = gamebox.from_color(random.randint(0, 800), random.randint(0,2) * 75 + 50, "yellow", 50, 50)

    # randomize their speed and direction
    enemy.xspeed = random.randint(3, 10)
    if random.randint(0,1) == 0:
        enemy.xspeed *= -1

    return enemy

def enemy_shoot_bullet(enemy, bullet):
    bullet.x = enemy.x
    bullet.y = enemy.y + 10
    bullet.speedy = 20

# bullet functions
def shoot_bullet(bullet):
    bullet.x = player.x
    bullet.y = 520
    bullet.speedy = 20

# score
score = 0

# game over screen
game_over_background = gamebox.from_color(400, 300, "black", 800, 600)

def tick(keys):

    global score

    # move player
    if pygame.K_LEFT in keys:
        player.x -= 10

    if pygame.K_RIGHT in keys:
        player.x += 10

    # shooting bullets
    if pygame.K_SPACE in keys and bullet1.yspeed == 0:
        shoot_bullet(bullet1)

    elif pygame.K_SPACE in keys and bullet2.yspeed == 0:
        shoot_bullet(bullet2)

    elif pygame.K_SPACE in keys and bullet3.yspeed == 0:
        shoot_bullet(bullet3)

    if pygame.K_SPACE in keys:
        keys.remove(pygame.K_SPACE)

    # moving bullets
    bullet1.y -= bullet1.speedy
    bullet2.y -= bullet2.speedy
    bullet3.y -= bullet3.speedy

    # stop bullet off screen
    if bullet1.y < 0:
        bullet1.speedy = 0
    if bullet2.y < 0:
        bullet2.speedy = 0
    if bullet3.y < 0:
        bullet3.speedy = 0

    # create enemies if there aren't any
    while len(enemies) < 3:
        enemies.append(create_enemy())

    # move the enemies
    for enemy in enemies:
        enemy.x += enemy.xspeed

    # reverse enemies if necessary
    for enemy in enemies:
        if enemy.x < 0:
            enemy.xspeed *= -1
        elif enemy.x > 800:
            enemy.xspeed *= -1

    # kill enemies with bullets
    for enemy in enemies:
        for bullet in bullets:
            if enemy.touches(bullet):
                enemy.x = random.randint(0, 800)
                enemy.y = random.randint(0,2) * 75 + 50
                enemy.xspeed = random.randint(3, 10)
                score += 1

    # enemy shoots bullets
    for i in range(len(en_bullets)):
        if en_bullets[i].yspeed == 0:
            enemy_shoot_bullet(enemies[i], en_bullets[i])

    # enemy bullets move
    for bullet in en_bullets:
        bullet.y += bullet.yspeed

    # handle bullets going off the screen
    for bullet in en_bullets:
        if bullet.y > 600:
            bullet.yspeed = 0

    # update the score
    score_display = gamebox.from_text(750, 10, str(score), "Arial", 12, "yellow")



    # draw everything
    camera.clear("black")
    camera.draw(player)
    camera.draw(bullet1)
    camera.draw(bullet2)
    camera.draw(bullet3)
    camera.draw(score_display)

    for bullet in en_bullets:
        camera.draw(bullet)

    for enemy in enemies:
        camera.draw(enemy)

    # game over
    for bullet in en_bullets:
        if bullet.touches(player):
            camera.draw(game_over_background)
            game_over_score = gamebox.from_text(400, 300, "Final Score: " + str(score), "Arial", 20, "yellow")
            camera.draw(game_over_score)
            gamebox.pause()

    camera.display()



ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, tick)