import pygame
import pyganim
from pygame.locals import *
import sys
import time

from bullet import Bullet

# some constants

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

front_standing = pygame.image.load('gameimages/crono_front.gif')
back_standing = pygame.image.load('gameimages/crono_back.gif')
left_standing = pygame.image.load('gameimages/crono_left.gif')
right_standing = pygame.transform.flip(left_standing, True, False)

playerWidth, playerHeight = front_standing.get_size()

animTypes = 'back_walk front_walk left_walk'.split()
animObjs = {}
for animType in animTypes:
  # 0.1 = duration
  imagesAndDurations = [('gameimages/crono_%s.%s.gif' % (animType, str(num).rjust(3, '0')), 0.1) for num in range(6)]
  animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)

MOVESPEED = 300

# create the right-facing sprites by copying and flipping the left-facing sprites
animObjs['right_walk'] = animObjs['left_walk'].getCopy()
animObjs['right_walk'].flip(True, False)
animObjs['right_walk'].makeTransformsPermanent()

moveConductor = pyganim.PygConductor(animObjs)

# start facing the user
direction = DOWN

class Player(pygame.sprite.Sprite):

   # running = moveUp = moveDown = moveLeft = moveRight = False
    

    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = front_standing
        self.rect = pygame.rect.Rect(location, self.image.get_size())

        self.resting = False
        self.dy = 0
        self.is_dead = False
        
        # gun cooldown
        self.gun_cooldown = 0
        self.moveUp = False
        self.moveDown = False
        self.moveRight = False
        self.moveLeft = False

    def update(self, dt, game):
        # copy of the old rect
        # used to check for the blockers
        last = self.rect.copy()

        #
        key = pygame.key.get_pressed()
        # change the location, 
        # direction to check which animation has to start          
        if key[pygame.K_LEFT]:
          self.rect.x -= MOVESPEED * dt
          self.direction = LEFT
          self.moveLeft = True
        if key[pygame.K_RIGHT]:
          self.rect.x += MOVESPEED * dt

          self.direction = RIGHT
          self.moveRight = True
        if key[pygame.K_UP]:
          self.rect.y -= MOVESPEED * dt
          self.direction = UP
          self.moveUp = True
        if key[pygame.K_DOWN]:
          self.rect.y += MOVESPEED * dt
          self.direction = DOWN
          self.moveDown = True


        if self.moveUp or self.moveDown or self.moveLeft or self.moveRight:
          moveConductor.play()
          if self.direction == UP:
          # ohne get currentframe() kommt error "must be pygameSurface not PygameAnimation"
            self.image = animObjs['back_walk'].getCurrentFrame()
          if self.direction == DOWN:
            self.image = animObjs['front_walk'].getCurrentFrame()
          if self.direction == LEFT:
            self.image = animObjs['left_walk'].getCurrentFrame()
          if self.direction == RIGHT:
            self.image = animObjs['right_walk'].getCurrentFrame()
        
        if key[pygame.K_LSHIFT] and not self.gun_cooldown:
          if self.direction == LEFT:
            Bullet(self.rect.midleft, LEFT, game.sprites)
          elif self.direction == RIGHT:
            Bullet(self.rect.midright, RIGHT, game.sprites)
          self.gun_cooldown = 1
      #     # shoot sound
          game.shoot.play()

        # kind of work around to deal with button release aka KEYUP without the pygame.event.get()
        # pygame.event.get() seems only to work in the main loop
        if str(key) == "(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)":
          # prevents players from pressing other keys and trigger the animation (because the moving is still true)
          self.moveLeft = self.moveRight = self.moveUp = self.moveDown = False
          if self.direction == LEFT:
            self.image = left_standing
          elif self.direction == RIGHT:
            self.image = right_standing
          elif self.direction == UP:
            self.image = back_standing
          elif self.direction == DOWN:
            self.image = front_standing
        
        #  moveConductor.stop()
        # shooting

        # 1 shot per second
        self.gun_cooldown = max(0, self.gun_cooldown - dt)
        # jump in the y axis, then decrease the y location of the player over time
        #if self.resting and key[pygame.K_SPACE]:
        #    game.jump.play()
        #    self.dy = -500
        #self.dy = min(400, self.dy + 40)

        #self.rect.y += self.dy * dt

        
        # deal with the triggers
        
        new = self.rect
        self.resting = False
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            blockers = cell['blockers']
            # check if the position before the update did not collide, then check if it now collides
            # e.g. new.right = 30 > cell.left = 25 -> collission, they overlap 
            if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            
            
            if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                self.dy = 0
         # see part of the doc chronotriggerish
            if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = (cell.bottom)
                self.dy = 0
        # enables the usual scrolling
        game.tilemap.set_focus(new.x, new.y)
