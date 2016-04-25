import pygame
import gamebox
import random
camera = gamebox.Camera(800, 600)

enemies = []

def create_enemy():
    enemy = gamebox.from_color(random.randint(0, 800), 50, "yellow", 50, 50)
    return enemy

def tick(keys):

    if pygame.K_SPACE in keys:
        enemies.append(create_enemy())

    camera.clear("black")

    for enemy in enemies:
        camera.draw(enemy)

    camera.display()

ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, tick)