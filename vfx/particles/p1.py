# squares
import pygame
import random

# Particle class
class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, col, amp):
        super().__init__()
        self.size = random.uniform(2, 5)
        self.image = pygame.Surface((self.size, self.size))
        cols = [col, (255, 255, 255)]
        random.choice
        self.image.fill(random.choice(cols))
        self.rect = self.image.get_rect(center=pos)
        self.vel = pygame.math.Vector2(random.uniform(-amp, amp), random.uniform(-amp, amp))
        self.gravity = 0  # Gravity effect
        self.fade_speed = random.uniform(0.5, 1)  # Fade speed
        self.alpha = 255


    def update(self):
        
        self.vel.y += self.gravity
        self.rect.move_ip(self.vel)
        self.alpha -= self.fade_speed
        #self.rect.inflate_ip(-self.rect.width*0.2, -self.rect.height*0.2)
        

        if self.alpha <= 0:
            self.kill()

        self.size += 0.1
        self.image = pygame.transform.scale(self.image, (int(self.size), int(self.size)))

    def draw(self, surface):
        self.image.set_alpha(int(self.alpha))
        surface.blit(self.image, self.rect.topleft)