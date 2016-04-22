import pygame
import gamebox
import random

# camera
camera = gamebox.Camera(800, 600)

# player ship
player_animations = gamebox.load_sprite_sheet("PlayerSprite.png", 1, 6)
player = gamebox.from_image(400, 550, player_animations[0])
# player = gamebox.from_color(400, 550, "red", 30, 30)

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

enemy_animations = gamebox.load_sprite_sheet("EnemySprite.png", 1, 6)

def create_enemy():
    # enemy = gamebox.from_color(random.randint(0, 800), random.randint(0,2) * 75 + 50, "yellow", 50, 50)
    enemy = gamebox.from_image(random.randint(0, 800), random.randint(0, 2) * 75 + 50, enemy_animations[0])

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

#sprite_counter for animations
sprite_counter = 0

# sound
death_sound = gamebox.load_sound("explosion.wav")
game_music = gamebox.load_sound("music1.wav")
music_player = game_music.play(-1)
bullet_sound = gamebox.load_sound("laser1.wav")
enemy_explosion_sound = gamebox.load_sound("finalenemyexplosion.wav")
lose_life_sound = gamebox.load_sound("loselifesound.wav")

# lives
life1 = gamebox.from_image(20, 20, "lifeimage.png")
life2 = gamebox.from_image(50, 20, "lifeimage.png")
life3 = gamebox.from_image(80, 20, "lifeimage.png")
lives = [True, True, True]

def lose_health():
    for i in range(len(lives)):
        if lives[i] == True:
            lives[i] = False
            break

def tick(keys):

    global score
    global sprite_counter

    # move player
    if pygame.K_LEFT in keys:
        player.x -= 10

    if pygame.K_RIGHT in keys:
        player.x += 10

    # shooting bullets
    if pygame.K_SPACE in keys and bullet1.yspeed == 0:
        shoot_bullet(bullet1)
        bullet_sound.play()

    elif pygame.K_SPACE in keys and bullet2.yspeed == 0:
        shoot_bullet(bullet2)
        bullet_sound.play()

    elif pygame.K_SPACE in keys and bullet3.yspeed == 0:
        shoot_bullet(bullet3)
        bullet_sound.play()

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
                enemy_explosion_sound.play(fade_ms = 100)

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
    score_display = gamebox.from_text(750, 10, str(score), "Algerian", 12, "yellow")

    # handle animations
    sprite_counter += 1
    if sprite_counter == 6:
        sprite_counter = 0


    player.image = player_animations[sprite_counter]
    for enemy in enemies:
        enemy.image = enemy_animations[sprite_counter]

    # play music
    music_player

    # draw everything
    camera.clear("black")
    camera.draw(player)
    camera.draw(bullet1)
    camera.draw(bullet2)
    camera.draw(bullet3)
    camera.draw(score_display)

    if lives[0] == True:
        camera.draw(life3)
    if lives[1] == True:
        camera.draw(life2)
    if lives[2] == True:
        camera.draw(life1)

    for bullet in en_bullets:
        camera.draw(bullet)

    for enemy in enemies:
        camera.draw(enemy)

    # game over
    for bullet in en_bullets:
        if bullet.touches(player):
            lose_health()
            bullet.yspeed = 0
            lose_life_sound.play()

    if lives[2] == False:
        camera.draw(game_over_background)
        game_over_score = gamebox.from_text(400, 300, "Final Score: " + str(score), "Algerian", 20, "yellow")
        camera.draw(game_over_score)
        death_sound.play()
        music_player.pause()
        gamebox.pause()

    camera.display()



ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, tick)