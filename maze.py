import astar
import grid
import random
from collections import deque

class Field(grid.Grid):
    def __init__(self, rows, columns, color):
        super().__init__(rows, columns, color, None)
        
    def _ToNumRepr(self):
        field = [[0 for j in range(self._columns)] for i in range(self._rows)]
        for i in range(0, len(self._objects)):
            for point in list(self._objects.items())[i][1]._coordinate_seq:
                field[point[1]][point[0]] = i + 1
        return field

class Maze(object):
    def _Walls_init(self, rows, columns, probability):
        maze = astar.createRandomizedLabirinth(rows, columns, probability)
        coordinate_seq = []
        for y in range(rows):
            for x in range(columns):
                if maze[y][x] == 1:
                    coordinate_seq += [(x, y)]
        return coordinate_seq 

    def __init__(self, rows, columns, probability, color):
        self._coordinate_seq = self._Walls_init(rows, columns, probability)
        self._color = color
        self._grid = None

class Dog(object):
    def __init__(self, starting_point, color):
        self._coordinate_seq = [starting_point]
        self._color = color
        self._grid = None
        self._path = deque()
        self._cell_color = (0, 0, 0)

    def FindPath(self, goal_point): 
        self._path = astar.astar(self._grid._ToNumRepr(), 
            self._coordinate_seq[0], goal_point)
        if self._path == -1:
            return False
        else:
            self._path = deque(self._path)
            return True

    def GetPath(self):
        return self._path

    def Go(self):
        if not self._path: return False
        self._grid._Put(self._coordinate_seq, self._grid._color)
        self._coordinate_seq[0] = self._path.popleft()
        self._grid._Put(self._coordinate_seq, self._color)
        return True

    def Hide(self):
        self._grid._Put(self._coordinate_seq, self._cell_color)

    def Appear(self):
        self._cell_color = self._grid._Get(self._coordinate_seq[0])
        self._grid._Put(coordinate_seq, self._color)

class Eagle(object):
    def __init__(self, point, color):
        self._coordinate_seq = [point] 
        self._color = color
        self._grid = None
        self._path = []
        self._cell_color = (0, 0, 0)

    def Hide(self):
        self._grid._Put(self._coordinate_seq, self._cell_color)

    def Appear(self, coordinate_seq = None): 
        if coordinate_seq == None: coordinate_seq = self._coordinate_seq
        self._coordinate_seq = coordinate_seq
        self._cell_color = self._grid._Get(self._coordinate_seq[0])
        self._grid._Put(coordinate_seq, self._color)

    def AppearRandom(self):
        self._coordinate_seq = [(random.randint(0, 1) * (self._grid._columns - 1),
                                 random.randint(0, 1) * (self._grid._rows - 1))]
        self._cell_color = self._grid._Get(self._coordinate_seq[0])
        self._grid._Put(self._coordinate_seq, self._color)

    def PathToDog(self):
       self._path = astar.astar(
            [[0 for j in range(self._grid._columns)] 
                for i in range(self._grid._rows)],
            self._coordinate_seq[0],
            self._grid._objects["Dog"]._coordinate_seq[0])

    def PickDog(self):
       self._cell_color = self._grid._color 

    def Move(self):
        if bool(self._path):
            self._grid._Put(self._coordinate_seq, self._cell_color)
            self._coordinate_seq = [self._path.popleft()]
            self._cell_color = self._grid._Get(self._coordinate_seq[0])
            self._grid._Put(self._coordinate_seq, self._color)
            return True
        else:
            return False

    def PathToRandPoint(self):
        point = (random.randint(0, self._grid._columns - 1),
            random.randint(0, self._grid._rows - 1))
        while self._grid._Get(point) != self._grid._color:
            point = (random.randint(0, self._grid._columns - 1),
                random.randint(0, self._grid._rows - 1))
            
        self._path = astar.astar(
            [[0 for j in range(self._grid._columns)] 
                for i in range(self._grid._rows)],
            self._coordinate_seq[0],
            point)

    def PathToRandCorner(self):
        point = (random.randint(0, 1) * (self._grid._columns - 1),
                 random.randint(0, 1) * (self._grid._rows - 1))
            
        self._path = astar.astar(
            [[0 for j in range(self._grid._columns)] 
                for i in range(self._grid._rows)],
            self._coordinate_seq[0],
            point)

    def PlaceDog(self):
        self._cell_color = self._grid._objects["Dog"]._color
        self._grid._objects["Dog"]._coordinate_seq = self._coordinate_seq
        self._grid._objects["Dog"]._path = []
