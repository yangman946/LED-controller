# lines
import pygame
import random
import os
import sys


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, col, amp):
        super().__init__()
        self.size = random.uniform(2, 5)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Transparent background

        cols = [col, (255, 255, 255)]
        self.color = random.choice(cols)
        self.a = amp

        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(random.uniform(-amp, amp), random.uniform(-amp, amp))
        self.fade_speed = random.uniform(0, 5)  # Fade speed: 0 slow 5 fast (fast wanna be thinner)

        r = min(self.fade_speed/4, 1)
        self.color = (self.color[0] * r, self.color[1] * r, self.color[2] * r)
        self.alpha = 255

        self.length = 1
        self.start_pos = self.pos.copy()



    def update(self):
        # Move the particle
        self.pos += self.vel
        self.length += self.a/10
        self.alpha -= self.fade_speed/2

        if self.alpha <= 0:
            self.kill()

    def draw(self, surface):
        if self.alpha > 0:
            end_pos = self.pos + self.vel * self.length
            
            pygame.draw.line(surface, self.color + (int(self.alpha),), self.start_pos + self.vel * (self.length - int(self.fade_speed)), end_pos, int(50/(self.a)))