from geometry import Point, Line, Cell
from tkinter import Button
import random
import time

ANIMATION_DELAY = 0.02

class Maze:
    def __init__(self, window=None, seed=None):
        self.window = window
        self.seed = seed
        
        if self.seed:
            self.seed = random.seed(seed)
        
        self._display_interface()
        
        self.num_rows = int(self.window.row_box.get())
        self.num_cols = int(self.window.col_box.get())
        self.cell_size = (int(self.window.canvas['height']) // self.num_rows) - 2
        
        self._generate_cells()

    def _display_interface(self):
        Button(
            self.window.canvas, 
            text='New', 
            width=5,
            height=2, 
            command=self._reset
        ).place(x=5, y=5)

        Button(
            self.window.canvas, 
            text='Solve', 
            width=5,
            height=2, 
            command=self._solve
        ).place(x=5, y=50)

    def _reset(self):
        items_to_remove = ['cell','move','undo']
        for items in items_to_remove:
            self.window.canvas.delete(items)
        
        self.num_rows = int(self.window.row_box.get())
        self.num_cols = int(self.window.col_box.get())
        self.cell_size = (int(self.window.canvas['height']) // self.num_rows) - 2
        
        self._generate_cells()
        self._draw_cells()
        self._create()
    
    def _generate_cells(self):
        self._cells = []
        for j in range(self.num_cols):
            for i in range(self.num_rows):
                cell = Cell(Point(i,j),Point(i+1,j+1))
                self._cells.append(cell)
        
        self._cells[0].tw = False
        self._cells[-1].bw = False
        
    def _draw_cells(self):

        canvas_midpoint = Line(
                Point(0,0),
                Point(int(self.window.canvas['width']), int(self.window.canvas['height']))
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

            cell.draw(self.window.canvas)
            self.window._redraw()
            time.sleep(ANIMATION_DELAY)

    def _create(self):

        def find_element(x, matrix):
            for i, row in enumerate(matrix):
                for j, element in enumerate(row):
                    if element == x:
                        return (i, j)
            return (-1, -1)

        def pick_open_neighbors(matrix, i, j):
            options = [-1, 1]
            open_neighbors = []
            for num in options:
                if 0 <= i+num <= self.num_rows:
                    try:
                        if not matrix[i+num][j].visited:
                            open_neighbors.append(matrix[i+num][j])
                    except:
                        continue
            for num in options:
                if 0 <= j+num <= self.num_cols:
                    try:
                        if not matrix[i][j+num].visited:
                            open_neighbors.append(matrix[i][j+num])
                    except:
                        continue
                    
            if open_neighbors:
                return random.choice(open_neighbors)
        
        def get_visited_cells(matrix, cell):
            
            visited = [cell]
            cell.visited = True
           
            i = find_element(cell, matrix)[0]
            j = find_element(cell, matrix)[1]
            while True:
                neighbor = pick_open_neighbors(matrix, i, j)
                if neighbor:
                    visited.append(neighbor)
                    neighbor.visited = True
                    i = find_element(neighbor, matrix)[0]
                    j = find_element(neighbor, matrix)[1]
            
                    if neighbor == matrix[-1][-1] or neighbor == matrix[0][0]:
                        break
                else:
                    visited.append(cell)
                    i = find_element(cell, matrix)[0]
                    j = find_element(cell, matrix)[1]
                    
                    if pick_open_neighbors(matrix, i, j) == None:
                        break
            return visited
            
        matrix = []
        for i in range (0, len(self._cells), self.num_cols):
            matrix.append(self._cells[i:i+self.num_cols])

        visited = []
        visited.append(get_visited_cells(matrix, matrix[0][0]))
        visited.append(get_visited_cells(matrix, matrix[-1][-1]))
        if self.num_cols > 12:
            visited.append(get_visited_cells(matrix, matrix[-1][0]))
            visited.append(get_visited_cells(matrix, matrix[0][-1]))
        
        self._break(visited)

    def _break(self, list):
        for cells in list:
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
                
                cells[i].draw(self.window.canvas, overwrite=True)
                self.window._redraw()
                time.sleep(ANIMATION_DELAY)

        cells[-1].draw(self.window.canvas, overwrite=True)

        for cel in self._cells:
            if not cel.visited:
                if cel.p1.x > self._cells[0].p1.x:
                   cel.lw = random.getrandbits(1)
                if cel.p2.x < self._cells[-1].p2.x:
                    cel.rw = random.getrandbits(1)
                if cel.p1.y > self._cells[0].p1.y:
                    cel.tw = random.getrandbits(1)
                if cel.p2.y < self._cells[-1].p2.y:
                    cel.bw = random.getrandbits(1)
        
                cel.draw(self.window.canvas, overwrite=True)      
    
    def _unvisit_cells(self):
        for cell in self._cells:
            cell.visited = False
    
    def _solve(self):
        self._unvisit_cells()
        self.window.canvas.delete('move')
        self.window.canvas.delete('undo')
    
        def draw_move(line, canvas, undo=False):
            
            tag = 'move'
            fill_color = 'red'
            
            if undo:
                tag = 'undo'
                fill_color = 'gray'
            
            Line.draw(
                Line(
                    Line(line.p1.p1, line.p1.p2).get_midpoint(),
                    Line(line.p2.p1, line.p2.p2).get_midpoint()
                ),
                canvas,
                fill_color,
                tag
            )
            self.window._redraw()
            time.sleep(.035)
    
        def _solve_r(matrix, i, j):
                
            matrix[i][j].visited = True
            if matrix[i][j] == matrix[-1][-1]:
                return True
            
            if (
                i > 0
                and (not matrix[i][j].tw
                or not matrix[i - 1][j].bw)
                and not matrix[i - 1][j].visited
            ):
                draw_move(Line(matrix[i][j], matrix[i - 1][j]),self.window.canvas)
                if _solve_r(matrix, i - 1, j):
                    return True
                else:
                    draw_move(Line(matrix[i][j], matrix[i - 1][j]),self.window.canvas,undo=True)

            if (
                i < self.num_rows - 1
                and not matrix[ i+ 1][j].tw
                and not matrix[i + 1][j].visited
            ):
                draw_move(Line(matrix[i][j], matrix[i + 1][j]),self.window.canvas)
                if _solve_r(matrix, i + 1, j):
                    return True
                else:
                    draw_move(Line(matrix[i][j], matrix[i + 1][j]),self.window.canvas,undo=True)

            if (
                j > 0
                and not matrix[i][j - 1].rw
                and not matrix[i][j - 1].visited
            ):
                draw_move(Line(matrix[i][j], matrix[i][j - 1]),self.window.canvas)
                if _solve_r(matrix, i, j - 1):
                    return True
                else:
                    draw_move(Line(matrix[i][j], matrix[i][j - 1]),self.window.canvas,undo=True)

            if (
                j < self.num_cols - 1
                and (not matrix[i][j + 1].lw
                or not matrix[i][j].rw)
                and not matrix[i][j + 1].visited
            ):
                draw_move(Line(matrix[i][j], matrix[i][j + 1]),self.window.canvas)
                if _solve_r(matrix, i, j + 1):
                    return True
                else:
                    draw_move(Line(matrix[i][j], matrix[i][j + 1]),self.window.canvas,undo=True)

            return False     

        matrix = []
        for i in range (0, len(self._cells), self.num_cols):
            matrix.append(self._cells[i:i+self.num_cols])
        
        return _solve_r(matrix, 0, 0)