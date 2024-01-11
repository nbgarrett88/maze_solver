from geometry import Point, Line, Cell
import random
import time

ANIMATION_DELAY = 0.015

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

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                cell = Cell(Point(i,j),Point(i+1,j+1))
                self._cells.append(cell)
        
        self._cells[0].tw = False
        self._cells[-1].bw = False
    
    def _draw_cells(self, canvas, win):

        canvas_midpoint = Line(
                Point(0,0),
                Point(int(canvas['height']), int(canvas['width']))
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

            cell.draw(canvas)
            win.update()
            time.sleep(ANIMATION_DELAY)

    def _break_walls_r(self):
        
        self._cells[0].visited = True
        visited = []

        return
