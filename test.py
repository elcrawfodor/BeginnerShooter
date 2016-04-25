import pygame
import gamebox

camera = gamebox.Camera(800, 600)
character = gamebox.from_color(50, 50, "red", 30, 60)
character.yspeed = 0
ground = gamebox.from_color(-100, 600, "black", 3000, 100)

def tick(keys):

    # moving left and right
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

    camera.clear("cyan")
    camera.draw(character)
    camera.draw(ground)

    #stop collisions with ground
    if character.bottom_touches(ground):
        character.yspeed = 0

    if character.touches(ground):
        character.move_to_stop_overlapping(ground)

    camera.display()

ticks_per_second = 30

#keep this line the last one in your program
gamebox.timer_loop(ticks_per_second,tick)