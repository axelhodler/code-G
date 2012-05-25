#from guernica import Player
import pygame

ENEMYSPEED = 100

class Enemy(pygame.sprite.Sprite):
    # the
    image = pygame.image.load('gameimages/enemy.png')
    # self ist das object welche die methoden nutzt #group = spritesgruppe
    def __init__(self, location, *groups):
        super(Enemy, self).__init__(*groups)
        # A Rect has a location and a size, size will be chosen by the image
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        # direction in which the enemy walks
        self.direction = 1

    def update(self, dt, game):
        # the enemy walks in the x direction (horizontal)
        self.rect.x += self.direction * ENEMYSPEED * dt
        # map ist aus cells aufgebaut, wenn self.rect mit nem reverse trigger collidet
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
            
            # nicht yber den trigger hinaus
            if self.direction > 0:
                self.rect.right = cell.left
            else:
                self.rect.left = cell.right
            # change direction
            self.direction *= -1
            break
        # check if enemy has collided with player
        if self.rect.colliderect(game.player.rect):
            game.player.is_dead = True
