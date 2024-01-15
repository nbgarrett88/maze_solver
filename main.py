from graphics import Window
from maze import Maze

def main():
    win = Window(600, 800)
    maze = Maze(win)
    
    maze._draw_cells()
    maze._create()
    maze._solve()
    
    win._wait_for_close()

if __name__ == '__main__':
    main()