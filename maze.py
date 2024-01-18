from geometry import Point, Line, Cell
from tkinter import Button
import random
import time

ANIMATION_DELAY = 0.025

class Maze:
    def __init__(self, window, seed=None):
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
        items_to_remove = ['cell','move']
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
        for j in range(self.num_rows):
            row_cells = []
            for i in range(self.num_cols):
                row_cells.append(Cell(Point(i,j),Point(i+1,j+1)))
            self._cells.append(row_cells)

        self._cells[0][0].tw = False
        self._cells[-1][-1].bw = False
        
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

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].p1.x = (self._cells[i][j].p1.x * self.cell_size) + shift_width
                self._cells[i][j].p2.x = (self._cells[i][j].p2.x * self.cell_size) + shift_width
                self._cells[i][j].p1.y = (self._cells[i][j].p1.y * self.cell_size) + shift_height
                self._cells[i][j].p2.y = (self._cells[i][j].p2.y * self.cell_size) + shift_height

                self._cells[i][j].draw(self.window.canvas)
                self.window._redraw()
                time.sleep(ANIMATION_DELAY)

    def _create(self):

        def find_element(x, matrix):
            for i, row in enumerate(matrix):
                for j, element in enumerate(row):
                    if element == x:
                        return (i, j)
            return (-1, -1)

        def pick_open_neighbors(i, j):
            options = [-1, 1]
            open_neighbors = []
            for num in options:
                if 0 <= i+num <= self.num_rows:
                    try:
                        if not self._cells[i+num][j].visited:
                            open_neighbors.append(self._cells[i+num][j])
                    except:
                        continue
            for num in options:
                if 0 <= j+num <= self.num_cols:
                    try:
                        if not self._cells[i][j+num].visited:
                            open_neighbors.append(self._cells[i][j+num])
                    except:
                        continue
                    
            if open_neighbors:
                return random.choice(open_neighbors)
        
        def get_visited_cells(cell):
            
            visited = [cell]
            cell.visited = True
           
            i = find_element(cell, self._cells)[0]
            j = find_element(cell, self._cells)[1]
            while True:
                neighbor = pick_open_neighbors(i, j)
                if neighbor:
                    visited.append(neighbor)
                    neighbor.visited = True
                    i = find_element(neighbor, self._cells)[0]
                    j = find_element(neighbor, self._cells)[1]
            
                    if neighbor == self._cells[-1][-1] or neighbor == self._cells[0][0]:
                        break
                else:
                    visited.append(cell)
                    i = find_element(cell, self._cells)[0]
                    j = find_element(cell, self._cells)[1]
                    
                    if pick_open_neighbors(i, j) == None:
                        break
            return visited

        visited = []
        visited.append(get_visited_cells(self._cells[0][0]))
        visited.append(get_visited_cells(self._cells[-1][-1]))
        if self.num_cols > 12:
            visited.append(get_visited_cells(self._cells[-1][0]))
            visited.append(get_visited_cells(self._cells[0][-1]))
        
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

        for i in range(self.num_rows-1):
            for j in range(self.num_cols-1):
                if not self._cells[i][j].visited:
                    if self._cells[i][j].p1.x > self._cells[0][0].p1.x:
                        if random.getrandbits(1):
                            self._cells[i][j].lw = False
                            self._cells[i][j-1].rw = False
                    if self._cells[i][j].p2.x < self._cells[-1][-1].p2.x:
                        if random.getrandbits(1):
                            self._cells[i][j].rw = False
                            self._cells[i][j+1].lw = False
                    if self._cells[i][j].p1.y > self._cells[0][0].p1.y:
                        if random.getrandbits(1):
                            self._cells[i][j].tw = False
                            self._cells[i-1][j].bw = False
                    if self._cells[i][j].p2.y < self._cells[-1][-1].p2.y:
                        if random.getrandbits(1):
                            self._cells[i][j].bw = False
                            self._cells[i+1][j].tw = False
            
                self._cells[i][j].draw(self.window.canvas, overwrite=True)
        self._cells[-1][-1].draw(self.window.canvas, overwrite=True)
    
    def _unvisit_cells(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False
    
    def _solve(self):
        self._unvisit_cells()
        self.window.canvas.delete('move')
    
        def draw_move(line, canvas, undo=False):
            
            fill_color = 'red'
            if undo:
                fill_color = 'gray'
            
            Line.draw(
                Line(
                    Line(line.p1.p1, line.p1.p2).get_midpoint(),
                    Line(line.p2.p1, line.p2.p2).get_midpoint()
                ),
                canvas,
                fill_color,
                tag='move'
            )
            self.window._redraw()
            time.sleep(ANIMATION_DELAY)
    
        def _solve_r(i, j):
                
            self._cells[i][j].visited = True
            if self._cells[i][j] == self._cells[-1][-1]:
                return True
            
            if (
                i > 0
                and not self._cells[i][j].tw
                and not self._cells[i - 1][j].visited
            ):
                draw_move(Line(self._cells[i][j], self._cells[i - 1][j]),self.window.canvas)
                if _solve_r(i - 1, j):
                    return True
                else:
                    draw_move(Line(self._cells[i][j], self._cells[i - 1][j]),self.window.canvas,undo=True)

            if (
                i < self.num_rows - 1
                and not self._cells[i][j].bw
                and not self._cells[i + 1][j].visited
            ):
                draw_move(Line(self._cells[i][j], self._cells[i + 1][j]),self.window.canvas)
                if _solve_r(i + 1, j):
                    return True
                else:
                    draw_move(Line(self._cells[i][j], self._cells[i + 1][j]),self.window.canvas,undo=True)

            if (
                j > 0
                and not self._cells[i][j].lw
                and not self._cells[i][j - 1].visited
            ):
                draw_move(Line(self._cells[i][j], self._cells[i][j - 1]),self.window.canvas)
                if _solve_r(i, j - 1):
                    return True
                else:
                    draw_move(Line(self._cells[i][j], self._cells[i][j - 1]),self.window.canvas,undo=True)

            if (
                j < self.num_cols - 1
                and not self._cells[i][j].rw
                and not self._cells[i][j + 1].visited
            ):
                draw_move(Line(self._cells[i][j], self._cells[i][j + 1]),self.window.canvas)
                if _solve_r(i, j + 1):
                    return True
                else:
                    draw_move(Line(self._cells[i][j], self._cells[i][j + 1]),self.window.canvas,undo=True)

            return False     

        return _solve_r(0, 0)