from geometry import Point, Line, Cell
from graphics import Window
import random
import time

ANIMATION_DELAY = 0.05

class Maze:
    def __init__(self, num_rows, num_cols, cell_size, window, seed=None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size = cell_size
        self.window = window
        self.seed = seed
        
        if self.seed:
            self.seed = random.seed(seed)

        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cell = Cell(Point(i,j),Point(i+1,j+1))
                self._cells.append(cell)
        
        self._cells[0].tw = False
        self._cells[-1].bw = False
        
    def _draw_cells(self, canvas, win):

        canvas_midpoint = Line(
                Point(0,0),
                Point(int(canvas['width']), int(canvas['height']))
            ).get_midpoint()
        
        maze_midpoint = Line(
                Point(0,0),
                Point(self.num_cols*self.cell_size, self.num_rows*self.cell_size)
            ).get_midpoint()
    
        shift_width = canvas_midpoint.x - maze_midpoint.x
        shift_height = canvas_midpoint.y - maze_midpoint.y

        for cell in self._cells:
            cell.p1.x = (cell.p1.x * self.cell_size) + shift_width
            cell.p2.x = (cell.p2.x * self.cell_size) + shift_width
            cell.p1.y = (cell.p1.y * self.cell_size) + shift_height
            cell.p2.y = (cell.p2.y * self.cell_size) + shift_height

            cell.draw(canvas)
            win.update()
            time.sleep(ANIMATION_DELAY)

    def _create_paths(self):

        def find_element(x, list):
            for i, row in enumerate(list):
                for j, element in enumerate(row):
                    if element == x:
                        return (i, j)
            return (-1, -1)

        def pick_open_neighbors(matrix, i, j):
            options = [-1,1]
            open_neighbors = []
            for num in options:
                if 0 <= i+num <= self.num_cols:
                    try:
                        if matrix[i+num][j].visited == False:
                            open_neighbors.append(matrix[i+num][j])
                    except:
                        continue
            for num in options:
                if 0 <= j+num <= self.num_rows:
                    try:
                        if matrix[i][j+num].visited == False:
                            open_neighbors.append(matrix[i][j+num])
                    except:
                        continue
                    
            if open_neighbors:
                return random.choice(open_neighbors)
        
        matrix = []
        for i in range (0, len(self._cells), self.num_cols):
            matrix.append(self._cells[i:i+self.num_cols])
        
        visited = [matrix[0][0]]
        matrix[0][0].visited = True
        i = 0
        j = 0
        while True:
            neighbor = pick_open_neighbors(matrix, i, j)
            if neighbor:
                visited.append(neighbor)
                neighbor.visited = True
                i = find_element(neighbor, matrix)[0]
                j = find_element(neighbor, matrix)[1]
                if neighbor == matrix[-1][-1]:
                    break
            else:
                break

        return visited

    def _solve(self, canvas, win, cells):

        for i in range(len(cells)-1):
            if cells[i].p1.x > cells[i+1].p1.x:
                cells[i].lw = False
                cells[i+1].rw = False
            elif cells[i].p1.x < cells[i+1].p1.x:
                cells[i].rw = False
                cells[i+1].lw = False
            elif cells[i].p1.y > cells[i+1].p1.y:
                cells[i].tw = False
                cells[i+1].bw = False
            elif cells[i].p1.y < cells[i+1].p1.y:
                cells[i].bw = False
                cells[i+1].tw = False
            cells[i].draw(canvas,overwrite=True)
            win.update()
            time.sleep(ANIMATION_DELAY)

        cells[i+1].draw(canvas,overwrite=True)

        for i in range(len(cells)-1):
            Window.draw_move(self.window,cells[i],cells[i+1])
            win.update()
            time.sleep(ANIMATION_DELAY)