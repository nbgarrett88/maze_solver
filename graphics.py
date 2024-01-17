from tkinter import Tk, Canvas, Label, Entry

class Window:
    def __init__(self, height, width):
        self.__running = False

        self.root = Tk()
        self.root.title('Maze Solver  |  Boot.dev  |  @nbgarrett88')
        self.root.protocol('WM_DELETE_WINDOW', self._close)

        self.canvas = Canvas(self.root, bg='white', height=height, width=width)
        self.canvas.pack(fill='both', expand=1)

        self.canvas.create_rectangle(0, 0, 75, height, fill='RoyalBlue')
        self.canvas.create_rectangle(width-75, 0, width, height, fill='RoyalBlue')

        Label(self.root, text='Rows:').place(x=5, y=100)
        self.row_box = Entry(self.root, width=3, justify='center')
        self.row_box.insert(0, '14')
        self.row_box.place(x=43, y=98)

        Label(self.root, text='Cols:').place(x=5, y=120)
        self.col_box = Entry(self.root, width=3, justify='center')
        self.col_box.insert(0, '14')       
        self.col_box.place(x=43, y=119)

    def _redraw(self):
        self.root.update_idletasks()
        self.root.update()
    
    def _wait_for_close(self):
        self.__running = True
        while self.__running:
            self._redraw()
        print('Window closed...')

    def _close(self):
        self.__running = False