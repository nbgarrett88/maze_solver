class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'Point({self.x},{self.y})'


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def __repr__(self):
        return f'Line(Point({self.p1.x},{self.p1.y}),Point({self.p2.x},{self.p2.y}))'
    
    def get_midpoint(self):
        return Point((self.p1.x + self.p2.x)/2, (self.p1.y + self.p2.y)/2)
    
    def draw(self, canvas, fill_color='black', tag=None):
        canvas.create_line(
            self.p1.x, self.p1.y, 
            self.p2.x, self.p2.y, 
            fill=fill_color, 
            width=3,
            tags=tag
        )

class Cell:
    def __init__(self, p1, p2, lw=True, rw=True, tw=True, bw=True, visited=False):
        self.p1 = p1
        self.p2 = p2
        self.lw = lw
        self.rw = rw
        self.tw = tw
        self.bw = bw
        self.visited = visited
    
    def __repr__(self):
        return f'Cell(Point({self.p1.x},{self.p1.y}),Point({self.p2.x},{self.p2.y}))'
        
    def draw(self, canvas, overwrite=False):
    
        if self.lw:
            Line(Point(self.p1.x, self.p1.y), Point(self.p1.x, self.p2.y)).draw(canvas,tag='cell')
        elif not self.lw and overwrite:
            Line(Point(self.p1.x, self.p1.y), Point(self.p1.x, self.p2.y)).draw(canvas,'white',tag='cell')
        
        if self.rw:
            Line(Point(self.p2.x, self.p2.y), Point(self.p2.x, self.p1.y)).draw(canvas,tag='cell')
        elif not self.rw and overwrite:
            Line(Point(self.p2.x, self.p2.y), Point(self.p2.x, self.p1.y)).draw(canvas,'white',tag='cell')
        
        if self.tw:
            Line(Point(self.p1.x, self.p1.y), Point(self.p2.x, self.p1.y)).draw(canvas,tag='cell')
        elif not self.tw and overwrite:
            Line(Point(self.p1.x, self.p1.y), Point(self.p2.x, self.p1.y)).draw(canvas,'white',tag='cell')
        
        if self.bw:
            Line(Point(self.p1.x, self.p2.y), Point(self.p2.x, self.p2.y)).draw(canvas,tag='cell')
        elif not self.bw and overwrite:
            Line(Point(self.p1.x, self.p2.y), Point(self.p2.x, self.p2.y)).draw(canvas,'white',tag='cell')