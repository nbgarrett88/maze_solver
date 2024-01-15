from tkinter import Tk, Canvas

class Window:
    def __init__(self, height, width):
        self.__root = Tk()
        self.__root.title('Maze Solver  |  Boot.dev  |  @nbgarrett88')
        self.__root.protocol('WM_DELETE_WINDOW', self._close)
        self.__running = False

        self.canvas = Canvas(self.__root, bg='white', height=height, width=width)
        self.canvas.pack(fill='both', expand=1)

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