# Michael Crawford (mdc8wa)

import pygame
import gamebox
import random

#camera
camera = gamebox.Camera(800, 600)

# player character
character = gamebox.from_color(400, 500, "red", 30, 60)
character.yspeed = 0

# health boxes
health1 = gamebox.from_color(50, 50, "red", 20, 20)
health2 = gamebox.from_color(100, 50, "red", 20, 20)
health3 = gamebox.from_color(150, 50, "red", 20, 20)
health = [True, True, True]

def lose_health():
    for i in range(len(health)):
        if health[i] == True:
            health[i] = False
            break

# game starting screen
game_start_background = gamebox.from_color(400, 300, "black", 800, 600)
game_start_text = gamebox.from_text(400, 300, "Press Space to play!", "Comic Sans MS", 30, "yellow")
game_start_condition = True
def change_game_start():
    return False

# game over screen
game_over_background = gamebox.from_color(400, 300, "black", 800, 600)
game_over_text = gamebox.from_text(400, 300, "You lose!", "Comic Sans MS", 30, "yellow")
win_game_over_text = gamebox.from_text(400, 300, "You win!", "Arial", 30, "yellow")

# enemy
enemy = gamebox.from_color(750, 50, "green", 30, 60)

# ground
ground = gamebox.from_color(-100, 600, "black", 3000, 100)

# coins
coin = gamebox.from_color(100, 525, "yellow", 10, 10)

# scores
char_counter = 0
enemy_counter = 0

def tick(keys):

    # make things global
    global char_counter
    global enemy_counter

    # character moving left and right
    if pygame.K_RIGHT in keys:
        character.x += 5
    if pygame.K_LEFT in keys:
        character.x -= 5

    # jumping
    if pygame.K_SPACE in keys and character.bottom_touches(ground):
        character.yspeed -= 17

    # gravity
    character.yspeed += 1
    character.y = character.y + character.yspeed

    enemy.yspeed += 1
    enemy.y = enemy.y + enemy.yspeed

    # enemy moves towards you
    if enemy.x > character.x:
        enemy.x -= 3

    else:
        enemy.x += 3

    # stop collisions with ground
    if character.bottom_touches(ground):
        character.yspeed = 0

    if character.touches(ground):
        character.move_to_stop_overlapping(ground)

    if enemy.bottom_touches(ground):
        enemy.yspeed = 0

    if enemy.touches(ground):
        enemy.move_to_stop_overlapping(ground)

    # character jumps on enemy
    if character.bottom_touches(enemy):
        enemy.x = 30
        enemy.y = 50
        enemy.yspeed = 0
        character.yspeed = -7

    # character gets hit on side
    if character.left_touches(enemy) or character.right_touches(enemy):
        enemy.x = 30
        enemy.y = 50
        enemy.yspeed = 0
        lose_health()

    # character touches coin
    if character.left_touches(coin) or character.right_touches(coin):
        coin.x = random.randint(100, 500)
        char_counter += 1

    # enemy touches coin
    if enemy.left_touches(coin) or enemy.right_touches(coin):
        coin.x = random.randint(100, 500)
        enemy_counter += 1


    # draw everything
    camera.clear("cyan")
    camera.draw(character)
    camera.draw(enemy)
    camera.draw(ground)
    camera.draw(coin)


    if health[0] == True:
        camera.draw(health1)
    if health[1] == True:
        camera.draw(health2)
    if health[2] == True:
        camera.draw(health3)

    # create score and draw it
    char_score = gamebox.from_text(700, 50, str(char_counter), "Comic Sans MS", 30, "red")
    enemy_score = gamebox.from_text(500, 50, str(enemy_counter), "Comic Sans MS", 30, "green")
    camera.draw(char_score)
    camera.draw(enemy_score)

    # game over screen
    if health[2] == False and char_counter <= enemy_counter:
        camera.draw(game_over_background)
        camera.draw(game_over_text)
        camera.draw(char_score)
        camera.draw(enemy_score)
        gamebox.pause()

    if health[2] == False and char_counter > enemy_counter:
        camera.draw(game_over_background)
        camera.draw(win_game_over_text)
        camera.draw(char_score)
        camera.draw(enemy_score)
        gamebox.pause()

    camera.display()

ticks_per_second = 30

#keep this line the last one in your program
gamebox.timer_loop(ticks_per_second,tick)