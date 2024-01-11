from graphics import Window
from maze import Maze

def main():
    win = Window(600, 800)
    maze = Maze(12,12,25)
    #maze = Maze(23,31,25,full_screen=True)
    
    win.draw_maze(maze)
    maze._break_walls_r
    win._wait_for_close()

if __name__ == '__main__':
    main()