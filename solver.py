from tkinter import Tk, Canvas

class Window:
    def __init__(self, height, width):
        self.__root = Tk()
        self.__root.title('Maze Solver')
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        self.__canvas = Canvas(self.__root, bg='white', height=height, width=width)
        self.__canvas.pack(fill='both', expand=1)
        self.__running = False
        
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print('Window closed...')

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)
    
    def draw_cell(self, cell):
        cell.draw(self.__canvas)

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

    def close(self):
        self.__running = False

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
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
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

    c1 = Cell(Point(50,50),Point(75,75), lw=False, rw=False)
    c2 = Cell(Point(75,50),Point(100,75), lw=False, bw=False)
    c3 = Cell(Point(75,75),Point(100,100), tw=False, bw=False)

    cells = [c1,c2,c3]

    for cell in range(len(cells)):
        win.draw_cell(cells[cell])
        if not cells[cell] == cells[-1]:
            win.draw_move(cells[cell],cells[cell+1])

    win.wait_for_close()

main()