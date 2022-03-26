from numpy import angle
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
    max_asteroids = 5
    asteroid_spawn_delay = 300
    laser_size = (5, 5)


class Timer(object):
    def __init__(self, duraton, with_start=True):
        self.duraton = duraton
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duraton

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duraton
            return True
        return False

class Background(object):
    def __init__(self, filename):
        self.image = pygame.image.load(os.path.join(
            Settings.path_image, filename))
        self.image = pygame.transform.scale(
            self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Spaceship(pygame.sprite.DirtySprite):
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
        self.check_border_collision()
        if pygame.sprite.spritecollide(self, game.asteroids, False):
            game.running = False
        self.dirty = 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_border_collision(self):
        if self.rect.top < -self.rect.height:
            self.rect.top = Settings.window_height

        elif self.rect.top > Settings.window_height + self.rect.height:
            self.rect.bottom = 0

        elif self.rect.left < -self.rect.width:
            self.rect.left = Settings.window_width

        elif self.rect.left > Settings.window_width + self.rect.width:
            self.rect.right = 0

    def shoot(self):
        if len(game.shots) < 10:
            Shot1 = Shot(self)
            game.shots.add(Shot1)
        
    

class Shot(pygame.sprite.DirtySprite):
    def __init__(self, spaceship):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, 'shot.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.laser_size)
        self.rect = self.image.get_rect()
        self.rect.center = spaceship.rect.center
        self.speed = 3
        self.lifetime = Timer(5000, False)
        self.max_shots = 10
        self.shots = []
        self.speed_x = 0
        self.speed_y = 0
        self.angle = spaceship.angle
    
    
    def update(self):
        if self.lifetime.is_next_stop_reached():
            self.kill()
        self.dirty = 1
        angle = radians(self.angle)
        self.speed_x = self.speed_x - sin(angle)
        if self.speed_x > 3:
            self.speed_x = 3
        self.speed_y = self.speed_y - cos(angle)
        if self.speed_y > 3:
            self.speed_y = 3
        self.rect.move_ip(self.speed_x, self.speed_y)



class Asteroids(pygame.sprite.DirtySprite   ):
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
        self.check_border_collision()
        self.dirty = 1

    def check_border_collision(self):
        if self.rect.top < -self.rect.height:
            self.rect.top = Settings.window_height

        elif self.rect.top > Settings.window_height + self.rect.height:
            self.rect.bottom = 0

        elif self.rect.left < -self.rect.width:
            self.rect.left = Settings.window_width

        elif self.rect.left > Settings.window_width + self.rect.width:
            self.rect.right = 0

    def move(self):
        self.rect.move_ip(*self.speed)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def spawn_position_finding(self):
        self.rect.left, self.rect.top = self.get_random_position()
        collided_asteroids = pygame.sprite.spritecollide(self, game.spaceship, False, pygame.sprite.collide_circle_ratio(3))
        if len(collided_asteroids) > 0:
            self.spawn_position_finding()

    def get_random_position(self):
        return random.randrange(0, Settings.window_width - self.rect.width), random.randrange(0, Settings.window_height - self.rect.height)

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.background = Background("background.jpg")
        self.spaceship = pygame.sprite.GroupSingle(Spaceship("3.png"))
        self.asteroids = pygame.sprite.LayeredDirty()
        self.asteroid_timer = Timer(Settings.asteroid_spawn_delay)
        self.running = True
        self.shots = pygame.sprite.LayeredDirty()

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
                    self.spaceship.sprite.turn_right()
                if event.key == pygame.K_LEFT:
                    self.spaceship.sprite.turn_left()
                if event.key == pygame.K_UP:
                    self.spaceship.sprite.move()
                if event.key == pygame.K_RETURN:
                    self.spaceship.sprite.shoot()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.spaceship.sprite.turn_right()
                if event.key == pygame.K_LEFT:
                    self.spaceship.sprite.turn_left()
                if event.key == pygame.K_UP:
                    self.spaceship.sprite.move()
                if event.key == pygame.K_KP_ENTER:
                    self.spaceship.sprite.shoot()


    def update(self):
        self.spaceship.sprite.update()
        self.asteroids.update()
        if self.asteroid_timer.is_next_stop_reached():
            if len(self.asteroids) < Settings.max_asteroids:
                self.asteroids.add(Asteroids(Settings.asteroid_images[random.randint(0, len(Settings.asteroid_images) - 1)], random.randint(*Settings.asteroid_size), (random.randint(*Settings.asteroid_speed), random.randint(*Settings.asteroid_speed)) ))
        self.shots.update()

    def draw(self):
        self.background.draw(self.screen)
        self.spaceship.sprite.draw(self.screen)
        self.asteroids.draw(self.screen)
        self.shots.draw(self.screen)

if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"

    game = Game()
    game.run()