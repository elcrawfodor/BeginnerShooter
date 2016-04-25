import pygame
import gamebox
camera = gamebox.Camera(800, 600)

def tick(keys):




    camera.display()

ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, tick)