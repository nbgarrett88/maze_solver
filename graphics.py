from tkinter import Tk, Canvas
from geometry import Line

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