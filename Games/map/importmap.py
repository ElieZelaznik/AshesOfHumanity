import pygame
import pytmx
from pytmx.util_pygame import*
import pyscroll

class GameMap:
    def __init__(self,screen_size):
        self.tmx_data = load_pygame('Games/ressource/map/map.tmx')
        self.map_layer = pyscroll.BufferedRenderer(pyscroll.data.TiledMapData(self.tmx_data), screen_size)
        self.map_layer.zoom = 1
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer,default_layer = 20) #permet de positionner le joueur a une hauteur précise
        
        self.walls = []

        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.walls.append(rect)
                
        
    def render(self, surface, center):
        self.map_layer.center(center)
        rect = surface.get_rect()
        self.map_layer.draw(surface, rect)