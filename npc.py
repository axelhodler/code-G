import pygame

CATSPEED = 50

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#standing pictures

class Cat(pygame.sprite.Sprite):
  
  image = pygame.image.load('gameimages/cat/cat_bw_left.png')
  
  def __init__(self, location, *groups):
    super(Cat, self).__init__(*groups)
    self.rect = pygame.rect.Rect(location, self.image.get_size())
    self.direction = 1

  def update(self, dt, game):
    
    last = self.rect.copy()
# walk towards the player
    self.rect.x += self.direction * CATSPEED * dt

    new = self.rect
    
    for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
      blockers = cell['blockers']
      
      if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
        new.right = cell.left
      if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
        new.left = cell.right
      if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
        new.bottom = cell.top
      if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
        new.top = cell.bottom
# animTypes 
# animObjs = {}

# for animType in animTypes:
#   # 0.1 = duration
#   imagesAndDurations = [('gameimages/cat_%s_%s.png' % (animType, str(num).rjust(3, '0')), 0.1) for num in range(6)]
#   animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)

