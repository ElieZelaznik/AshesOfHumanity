import pygame
import pytmx
from pytmx.util_pygame import*
import pyscroll

class GameMap:
    def __init__(self,screen_size):
        self.tmx_data = load_pygame('games/ressource/map/map.tmx')
        self.map_layer = pyscroll.BufferedRenderer(pyscroll.data.TiledMapData(self.tmx_data), screen_size)
        self.map_layer.zoom = 1
        
    def render(self, surface, center):
        self.map_layer.center(center)
        rect = surface.get_rect()
        self.map_layer.draw(surface, rect)