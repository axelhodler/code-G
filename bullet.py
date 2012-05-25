import pygame

BULLETSPEED = 500
LEFT = 'left'
RIGHT = 'right'

class Bullet(pygame.sprite.Sprite):
    image = pygame.image.load('bullet.png')
    def __init__(self, location, direction, *groups):
        super(Bullet, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.direction = direction
        self.lifespan = 2

    def update(self, dt, game):
        self.lifespan -= dt
        if self.lifespan < 0:
            self.kill()
            return
        if self.direction == LEFT:
          self.rect.x += -1 * BULLETSPEED * dt
        elif self.direction == RIGHT:
          self.rect.x += 1 * BULLETSPEED * dt
        # check collision
        if pygame.sprite.spritecollide(self, game.enemies, True):
            game.explosion.play()
            self.kill()
