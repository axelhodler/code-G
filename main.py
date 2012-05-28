# the soundfiles were taken from soundbible.com
# 
# the two shotgun files:
# License: Attribution 3.0 | Recorded by RA The Sun God
#
# the current basic structure was taken from 
# Introduction to Game Development by Richard Jones
# http://www.youtube.com/watch?v=duc3jYgAaR0
#
# some chrono trigger sprites were take from http://videogamesprites.net/


# tiled shit has to be in the same folder as the fucking tmx.py 8[[[
# TODO change that shit

import pygame
import tmx

from enemy import Enemy
from player import Player
from npc import Cat

class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()

        # tiled part
        self.tilemap = tmx.load('tiled/map.tmx', screen.get_size())

        self.sprites = tmx.SpriteLayer()
        # get the start cell in the map and set the player position accordingly
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)
        
        # enemies
        self.enemies = tmx.SpriteLayer()
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            Enemy((enemy.px, enemy.py), self.enemies)
        self.tilemap.layers.append(self.enemies)
        
        # cat
        self.cat = tmx.SpriteLayer()
        for cats in self.tilemap.layers['cat'].find('cat'):
          Cat((cats.px, cats.py), self.cat)
        self.tilemap.layers.append(self.cat)
        
        # weapon sound
        self.shoot = pygame.mixer.Sound('sounds/weapons/shotgun_shot.wav')
        self.reload = pygame.mixer.Sound('sounds/weapons/shotgun_reload.wav')
        
        # gameloop
        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.tilemap.update(dt / 1000., self)
            self.tilemap.draw(screen)
            pygame.display.flip()
            
            # whatever
            if self.player.is_dead:
                print 'U DYED......... YOUR SHIRT RED'
                return

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("insert gamename")
    Game().main(screen)

