'''
Provides Concrete EventManager class and Abstract 
EventListener class for controlling game pygame events.
'''

import re
import pygame


def camel_to_snake(name: str):
    '''takes the name and converts it to snake case'''
    name = re.sub(R'(?<!^)(?=[A-Z])', '_', name).lower()
    return name


class EventManager():
    '''
    Provides a concrete class for objects to register themselves as listeners
    to, so that they can easily execute code on pygame events.
    '''

    def __init__(self):
        self.__listeners = {}

    def notify(self, event):
        '''
        Calls corresponding snake case style on_<event_name> methods
        of all EventListener objects that have registered to this
        Event Manager.
        '''
        if self.__listeners.get(event.type):
            for listener in self.__listeners[event.type]:
                listener.do_event(event)

    def add_listener(self, listener, *event_types):
        for event_type in event_types:
            if not self.__listeners.get(event_type):
                self.__listeners[event_type] = []

            self.__listeners[event_type].append(listener)


class EventListener:

    def __init__(self):
        self.custom_event_functions = {}

    def on_event(self, event_type, function):
        if not self.custom_event_functions.get(event_type):
            self.custom_event_functions[event_type] = []

        self.custom_event_functions[event_type].append(function)

    def do_event(self, event):
        '''
        Calls the corresponding on_<event_snake_case>(event)
        method in this listener, if such a method has been
        implemented. Also calls all custom named functions
        added via on_event(event, function) method.
        '''
        # call default-named functions if they exist:
        event_name_snake_case = camel_to_snake(
            pygame.event.event_name(event.type)
        )
        for member in dir(self):
            if member == "on_{}".format(event_name_snake_case):
                attr = getattr(self, member)
                attr(event)

        # Call custom-named functions:
        if self.custom_event_functions.get(event.type):
            for function in self.custom_event_functions[event.type]:
                function(event)
