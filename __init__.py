'''module for starting the game'''

import os
import sys
import pygame
from . import event as eventmodule
from .event import EventListener, EventManager
from .drawing import DrawManager
from .entity import Entity
from . import defaultcolors

def clear_entities():
    draw_manager = DrawManager()
    event_manager = EventManager()
    
def add_entity(entity):
    draw_manager.add_drawing(entity)
    event_manager.add_listener(entity)
    
def remove_entity(entity):
    draw_manager.remove_drawing(entity)
    event_manager.remove_listener(entity)

def init(resolution, fullscreen=False, color_scheme=None):
    pygame.init()
    
    if fullscreen:
        pygame.display.set_mode(resolution, flags=pygame.FULLSCREEN)
    else:
        pygame.display.set_mode(resolution)
    
    # override default colors module if a color
    # scheme is passed in:
    if color_scheme:
        _color_scheme = color_scheme

def start_game():
    
    draw_manager.add_drawing(cursor)
    event_manager.add_listener(cursor, pygame.WINDOWLEAVE, pygame.WINDOWENTER)
    
    clock = pygame.time.Clock()
    while True:
        
        # process events and draws:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return
            
            event_manager.notify(event)
            draw_manager.draw_all()  

        # keeps the framerate from going to high (but not too low, low depends on our code)
        clock.tick(60)
        pygame.event.post(pygame.event.Event(eventmodule.TICK))
        
        # displays all the graphical updates that have been made.
        pygame.display.flip()

class _Cursor (Entity, EventListener):
    
    def __init__(self):
        Entity.__init__(self, pygame.rect.Rect(0, 0, 0, 0))
        EventListener.__init__(self)
        self.image = None
        self.set_draw_method(self._draw)
    
    def set_image(self, filepath):
        if filepath is None: 
            pygame.mouse.set_visible(True)
            self.image = None
        else:
            abs_filepath = os.path.abspath(filepath)
            pygame.mouse.set_visible(False)
            self.image = pygame.image.load(abs_filepath)
            self.image = pygame.transform.scale(self.image, (25, 25))
            self.rect = self.image.get_rect()
        
    def _draw(self, screen):
        if self.image:
            x, y = pygame.mouse.get_pos()
            x -= 10
            y -= 5
            self.rect.topleft = (x, y)
            screen.blit(self.image, self.rect.topleft)
    
    def on_window_leave(self, event):
        self.set_visible(False)
        
    def on_window_enter(self, event):
        self.set_visible(True)

# globals:
cursor = _Cursor()
draw_manager = DrawManager()
event_manager = EventManager()

# package private globals:
_color_scheme = defaultcolors
