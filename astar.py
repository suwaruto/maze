# A* pathfinding algo

from random import uniform
from collections import deque

def _mazeOutput( maze ):
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            print(maze[i][j], end = ' ')
        print()
        
def mazeInsertPath( maze, path ):
    for item in path:
        maze[item[1]][item[0]] = '*'
    return maze

def createRandomizedLabirinth( n, m, p ):
    lst = []
    for i in range (0, n):
        row = []
        for j in range (0, m):
            if uniform(0, 1) < p:
                row += [1]
            else:
                row += [0]
        lst += [row]
    return lst
    
def _createMap( n, m, fill ):
    res = []
    for i in range(0, n):
        row = []
        for j in range(0, m):
            row += [fill]
        res += [row]
    return res
    
def _heuristic( p1, p2 ):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
def _isOnMap( point, n, m ):
    if point[0] < 0 or point[1] < 0 or point[0] >= m or point[1] >= n:
        return False
    else:
        return True
        
def _isInDeq( dq, node ):
    for i in dq:
        if node == i:
            return True
    return False
    
def _reconstruct_path( camefrom, current, start ):
    total_path = deque([current])
    while not (current is start):
        current = camefrom[current[1]][current[0]]
        total_path.appendleft(current)
    return total_path
    
def astar( maze, start, goal ):
    n = len(maze)
    m = len(maze[0])
    opendeque = deque([start])
    camefrom = _createMap(n, m, 0)
    gScore = _createMap(n, m, n * m)
    gScore[start[1]][start[0]] = 0
    fScore = _createMap(n, m, n * m)
    fScore[start[1]][start[0]] = _heuristic(start, goal)
    
    while len(opendeque) != 0:
        current = opendeque.popleft()
        if current == goal:
            return _reconstruct_path(camefrom, current, start)
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbour = (current[0] + j, current[1] + i)
                if _isOnMap(neighbour, n, m) and maze[neighbour[1]][neighbour[0]] != 1 \
                and neighbour != current:
                    tentative_gScore = gScore[current[1]][current[0]] + 1
                    if tentative_gScore < gScore[neighbour[1]][neighbour[0]]:
                        camefrom[neighbour[1]][neighbour[0]] = current
                        gScore[neighbour[1]][neighbour[0]] = tentative_gScore
                        fScore[neighbour[1]][neighbour[0]] = gScore[neighbour[1]][neighbour[0]] + \
                            _heuristic(neighbour, goal)
                        if not _isInDeq(opendeque, neighbour):
                            opendeque.appendleft(neighbour)
                        # deque correction
                        for k in range(1, len(opendeque) + 1):
                            if k >= len(opendeque):
                                opendeque.append(opendeque.popleft())
                            elif fScore[opendeque[0][1]][opendeque[0][0]] <= \
                            fScore[opendeque[i][1]][opendeque[i][0]]:
                                opendeque.insert(i, opendeque.popleft())
                                break        
    return -1
    
    
    
def main():
    n, m, p = input("Enter quantity of rows, quantity of columns and wall probability: ").split(' ', 2)
    start = input("Enter the start point's coordinates x y: ")
    goal = input("Enter the goal point's coordinates x y: ")
    n = int(n)
    m = int(m)
    p = float(p)
    start = (int(start.split(' ', 1)[0]), int(start.split(' ', 1)[1])) 
    goal = (int(goal.split(' ', 1)[0]), int(goal.split(' ', 1)[1])) 
    lst = createRandomizedLabirinth(n, m, p)
    _mazeOutput(lst)
    path = astar(lst, start, goal)
    print(path)
    _mazeOutput(mazeInsertPath(lst, path))
if __name__ == '__main__': main()
