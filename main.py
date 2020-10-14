import astar
import pygame
import maze

def HandleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def main():
    window = pygame.display.set_mode((300, 300))
    field = maze.Field(20, 20, (0, 0, 0))
    walls = maze.Maze(20, 20, 0.35, (255, 255, 255))
    field.Register("Maze", walls)
    dog = maze.Dog((0, 0), (0, 0, 255))
    field.Register("Dog", dog)
    eagle = maze.Eagle((19, 19), (0, 255, 0)) 
    field.Register("Eagle", eagle)
    eagle.Hide()
    
    field.Draw(window)
    pygame.display.update()

    running = True
    while running:
        running = HandleEvents()
        if bool(dog.GetPath()):
            pygame.time.wait(250)
            dog.Go()
            field.Draw(window)
            pygame.display.update()
        else:
            if not dog.FindPath((19, 19)):
                pygame.time.wait(1000)
                eagle.Appear()
                eagle.PathToDog()
                
                while running and eagle.Move():
                    running = HandleEvents()
                    pygame.time.wait(250)
                    field.Draw(window)
                    pygame.display.update()
                
                if running:
                    eagle.PickDog()
                    eagle.PathToRandPoint()

                while running and eagle.Move():
                    running = HandleEvents()
                    pygame.time.wait(250)
                    field.Draw(window)
                    pygame.display.update()

                if running:
                    eagle.PlaceDog()
                    eagle.PathToRandCorner()

                while running and eagle.Move():
                    running = HandleEvents()
                    pygame.time.wait(250)
                    field.Draw(window)
                    pygame.display.update()

                if running: eagle.Hide()

if __name__ == '__main__': main()
