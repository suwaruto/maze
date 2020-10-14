import pygame
from collections import OrderedDict

class Grid(object):
    def __init__(self, rows, columns, color, grid = None):
        self._rows = rows
        self._columns = columns
        self._color = color
        if not (grid is None):
            self._grid = grid[:][:]
        else: 
            self._grid = []
            for y in range(self._rows):
                row = []
                for x in range(self._columns):
                    row += [self._color]
                self._grid += [row]
        self._objects = OrderedDict()

    def _Put(self, coordinate_seq, color):
        for item in coordinate_seq:
           self._grid[item[1]][item[0]] = color 

    def _Get(self, point):
        return self._grid[point[1]][point[0]]

    def Register(self, key, obj, color = None):
        if color == None:
            color = obj._color
        self._objects[key] = obj
        obj._grid = self
        self._Put(obj._coordinate_seq, color)

    def Draw(self, surface):
        width = surface.get_width()  
        height = surface.get_height()
        step_x = width // self._columns
        step_y = height // self._rows
        for y in range(self._rows):
            for x in range(self._columns):
                pygame.draw.rect(surface, self._grid[y][x],
                    pygame.Rect(x * step_x, y * step_y, step_x, step_y))
