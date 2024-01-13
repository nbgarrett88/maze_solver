from graphics import Window
from maze import Maze

def main():
    win = Window(600, 800)
    maze = Maze(10,10,50,win,seed=1)
    win.draw_maze(maze)
    paths = maze._create_paths()
    win.solve_maze(maze,paths)
    win._wait_for_close()

if __name__ == '__main__':
    main()