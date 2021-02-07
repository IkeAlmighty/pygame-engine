from abc import ABC
import pygame

class Drawing(ABC):

    def __init__(self, rect: pygame.rect.Rect):
        self._draw_method = lambda scr: None
        self.rect = rect
        self.last_draw_rect = None
        self._visible = True

    def set_draw_method(self, method):
        self._draw_method = method

    def do_draw_method(self):
        screen = pygame.display.get_surface()
        self._draw_method(screen)
        self.last_draw_rect = self.rect.copy()
        
    def set_visible(self, visible):
        self._visible = visible
    
    def get_visible(self):
         return self._visible

class DrawManager:
    
    def __init__(self):
        self._collision_map = {} # maps an drawing to entities that collide with it
        self._queue = [] # holds a queue of entities that need to be redrawn
    
    def _register_drawing_collisions(self, new_drawing):
        # find all entities that collied with this new drawing,
        # and also add this new enitity to their collision lists.
        new_drawing_collisions = []
        for drawing in self._collision_map.keys():
            if drawing.rect.colliderect(new_drawing.rect):
                new_drawing_collisions.append(drawing)
                self._collision_map[drawing].append(new_drawing)
                
        self._collision_map[new_drawing] = new_drawing_collisions
    
    def add_drawing(self, *args):
        for drawing in args:
            if not self._collision_map.get(drawing):
                self._register_drawing_collisions(drawing)
                
            self._queue.append(drawing)
    
    def remove_drawing(self, *args):
        for drawing in args:
            self._collision_map.pop(drawing, None)
            for key_drawing in self._collision_map.keys():
                if drawing in self._collision_map[key_drawing]:
                    self._collision_map[key_drawing].remove(drawing)
            
            self._queue.remove(drawing)
                        
    def draw_all(self):
        redraw_queue = []
        for drawing in self._queue:
            # if the drawing is not on screen, don't draw it:
            # make a rect slightly larger than the screen to avoid edge of screen entities:
            screen_rect = pygame.display.get_surface().get_rect().copy()
            screen_rect.x -= 50
            screen_rect.y -= 50
            screen_rect.width += 100
            screen_rect.height += 100
            if not drawing.rect.colliderect(screen_rect):
                continue
            
            # erase (if it's been drawn once),
            if drawing.last_draw_rect:
                pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), drawing.last_draw_rect)
            
            # add collisions to redraw queue:
            collision_update_queue = []
            for collision in self._collision_map[drawing]:
                redraw_queue.append(collision)
                # flag update for collision map:
                if not drawing.rect.colliderect(collision.rect):
                    collision_update_queue.append(collision)
            
            # update the collision map:
            for collision in collision_update_queue:
                self._collision_map[drawing].remove(collision)
                self._collision_map[collision].remove(drawing)
            
            # add this drawing to the end of the redraw queue:
            if drawing.get_visible():
                redraw_queue.append(drawing)
            
        # redraw everything added to the redraw queue
        # (this will include all of the initial _queue entities + their collisions):
        # print('redraw queue:', redraw_queue)
        for drawing in redraw_queue:
            drawing.do_draw_method()