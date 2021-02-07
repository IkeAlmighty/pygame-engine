import pygame
from .drawing import Drawing
from .event import EventListener
import sys

class Entity(Drawing, EventListener):

    def __init__(self, rect: pygame.rect.Rect):
        Drawing.__init__(self, rect)
        EventListener.__init__(self)
        
            
class EntityContainer(Drawing):
    '''
    A way to easily group many entities together.
    '''
    
    def __init__(self, *entities):
        Entity.__init__(self, pygame.rect.Rect(0, 0, 0, 0))
        self.__children = []
        
        for child in entities:
            self.add_child(child)
        
    def add_child(self, entity: Entity):
        self.__children.append(entity)
        
        # adjust the bounding rect for this container
        self.rect.topleft = self.__find_topleft()
        bottomright = self.__find_bottomright()
        self.rect.size = (bottomright[0] - self.rect.x, bottomright[1] - self.rect.y)
    
    def __find_topleft(self):
        lowest_x, lowest_y = sys.maxsize, sys.maxsize
        for child in self.__children:
            if child.rect.x < lowest_x:
                lowest_x = child.rect.x
            if child.rect.y < lowest_y:
                lowest_y = child.rect.y
        
        return (lowest_x, lowest_y)
            
    
    def __find_bottomright(self):
        highest_x, highest_y = -1 * sys.maxsize, -1 * sys.maxsize
        for child in self.__children:
            if child.rect.x > highest_x:
                highest_x = child.rect.x
            if child.rect.y > highest_y:
                highest_y = child.rect.y
        
        return (highest_x, highest_y)
    
    def do_draw_method(self):
        super(EntityContainer, self).do_draw_method()
        for child in self.__children:
            child.do_draw_method()