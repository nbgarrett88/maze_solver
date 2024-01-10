from tkinter import Tk, Canvas
import random
import time

ANIMATION_DELAY = 0.01

class Window:
    def __init__(self, height, width):
        self.__root = Tk()
        self.__root.title('Maze Solver  |  Boot.dev  |  @nbgarrett88')
        self.__root.protocol('WM_DELETE_WINDOW', self._close)
        self.__canvas = Canvas(self.__root, bg='white', height=height, width=width)
        self.__canvas.pack(fill='both', expand=1)
        self.__running = False
        
    def _redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def _wait_for_close(self):
        self.__running = True
        while self.__running:
            self._redraw()
        print('Window closed...')

    def _close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)
    
    def draw_cell(self, cell):
        cell.draw(self.__canvas)
    
    def draw_maze(self, maze):
        maze._draw_cells(self.__canvas, self.__root)

    def draw_move(self, cell, to_cell, undo=False):

        if undo:
            fill_color = 'gray'
        else:
            fill_color = 'red'
        
        self.draw_line(
            Line(
                Line(cell.p1,cell.p2).get_midpoint(),
                Line(to_cell.p1,to_cell.p2).get_midpoint()
            ),
            fill_color
        )


class Maze:
    def __init__(self, num_rows, num_cols, cell_size, full_screen=False, seed=None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size = cell_size
        self.full_screen = full_screen
        self.seed = seed
        
        if self.seed:
            self.seed = random.seed(seed)

        self._create_cells()
        self._break_walls_r()

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                cell = Cell(Point(i,j),Point(i+1,j+1))
                self._cells.append(cell)
    
    def _draw_cells(self, canvas, win):

        canvas_midpoint = Line(
                Point(0,0),
                Point(int(canvas['height']),int(canvas['width']))
            ).get_midpoint()
        maze_midpoint = Line(
                Point(0,0),
                Point(self.num_cols*self.cell_size, self.num_rows*self.cell_size)
            ).get_midpoint()
    
        shift_height = canvas_midpoint.x - maze_midpoint.x
        shift_width = canvas_midpoint.y - maze_midpoint.y

        if self.full_screen:
            shift_height = 12 
            shift_width = 16

        for cell in self._cells:
            cell.p1.x = (cell.p1.x * self.cell_size) + shift_width
            cell.p2.x = (cell.p2.x * self.cell_size) + shift_width
            cell.p1.y = (cell.p1.y * self.cell_size) + shift_height
            cell.p2.y = (cell.p2.y * self.cell_size) + shift_height
            
            if cell == self._cells[0]:
                cell.tw = False
            elif cell == self._cells[-1]:
                cell.bw = False

            cell.draw(canvas)
            win.update()
            time.sleep(ANIMATION_DELAY)

    def _break_walls_r(self):
        
        self._cells[0].visited = True
        visited = []

        return


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def get_midpoint(self):
        return Point((self.p1.x + self.p2.x)/2,(self.p1.y + self.p2.y)/2)
    
    def draw(self, canvas, fill_color='black'):
        canvas.create_line(
            self.p1.x, self.p1.y, 
            self.p2.x, self.p2.y, 
            fill=fill_color, 
            width=2
        )
        canvas.pack(fill='both', expand=True)


class Cell:
    def __init__(self, p1, p2, lw=True, rw=True, tw=True, bw=True, visited=False):
        self.p1 = p1
        self.p2 = p2
        self.lw = lw
        self.rw = rw
        self.tw = tw
        self.bw = bw
        self.visited = visited
        
    def draw(self, canvas):
        if self.lw:
            Line(Point(self.p1.x, self.p1.y), Point(self.p1.x, self.p2.y)).draw(canvas)
        if self.rw:
            Line(Point(self.p2.x, self.p2.y), Point(self.p2.x, self.p1.y)).draw(canvas)
        if self.tw:
            Line(Point(self.p1.x, self.p1.y), Point(self.p2.x, self.p1.y)).draw(canvas)
        if self.bw:
            Line(Point(self.p1.x, self.p2.y), Point(self.p2.x, self.p2.y)).draw(canvas)
    

def main():
    win = Window(600, 800)
    maze = Maze(20,20,25)
    #maze = Maze(23,31,25,full_screen=True)
    win.draw_maze(maze)
    win._wait_for_close()

if __name__ == '__main__':
    main()