import pygame
import os
from math import cos, sin, radians
import random

class Settings(object):
    window_width = 800
    window_height = 500
    fps = 60
    path_image = os.path.join(os.path.dirname(__file__), "images")
    title = "Asteroids"
    spaceship_size = (30, 24)
    border_size = (30)
    asteroid_images = ['0.png', '1.png', '2.png', '5.png', '6.png', '7.png', '8.png', '9.png'] 
    asteroid_size = (10, 30)
    asteroid_speed = (-5, 5)

class Background(object):
    def __init__(self, filename):
        self.image = pygame.image.load(os.path.join(
            Settings.path_image, filename))
        self.image = pygame.transform.scale(
            self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.update_sprite(self.filename)
        self.rect.left = Settings.window_width // 2 - self.rect.width // 2
        self.rect.top =  Settings.window_height // 2 - self.rect.height // 2
        self.angle = 0
        self.speed_x = 0
        self.speed_y = 0

    def turn_left(self):
        self.angle += 22.5
        center = self.rect.center
        self.update_sprite(self.filename, self.angle)
        self.rect.center = center

    def turn_right(self):
        self.angle -= 22.5
        center = self.rect.center
        self.update_sprite(self.filename, self.angle)
        self.rect.center = center

    def update_sprite(self, filename, angle=None):
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.spaceship_size)
        if angle != None:
            self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        
    def move(self):
        angle = radians(self.angle)
        self.speed_x = self.speed_x - sin(angle)
        if self.speed_x > 10:
            self.speed_x = 10
        self.speed_y = self.speed_y - cos(angle)
        if self.speed_y > 10:
            self.speed_y = 10

    def accelerating(self):
        self.rect.move_ip(self.speed_x, self.speed_y)

    def update(self):
        self.accelerating()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Asteroids(pygame.sprite.Sprite):
    def __init__(self, filename, size, speed):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(0, Settings.window_width)
        self.rect.top = random.randrange(0, Settings.window_height)
        self.timer = 0
        self.speed = speed
        
    def update(self):
        self.move()
        if self.rect.left >= Settings.window_width:
            self.rect.left = 0
        if self.rect.top >= Settings.window_height:
            self.rect.top = 0

    def move(self):
        self.rect.move_ip(*self.speed)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.background = Background("background.jpg")
        self.spaceship = Spaceship("3.png")
        self.asteroids = pygame.sprite.Group()
        for i in range(5):
            self.asteroids.add(Asteroids(Settings.asteroid_images[random.randint(0, len(Settings.asteroid_images) - 1)], random.randint(*Settings.asteroid_size), (random.randint(*Settings.asteroid_speed), random.randint(*Settings.asteroid_speed)) ))
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.draw()
            self.update()
            pygame.display.flip()
        pygame.quit() 


    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.spaceship.turn_right()
                if event.key == pygame.K_LEFT:
                    self.spaceship.turn_left()
                if event.key == pygame.K_UP:
                    self.spaceship.move()

    def update(self):
        self.spaceship.update()
        self.asteroids.update()
    
    def draw(self):
        self.background.draw(self.screen)
        self.spaceship.draw(self.screen)
        self.asteroids.draw(self.screen)

if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"

    game = Game()
    game.run() 