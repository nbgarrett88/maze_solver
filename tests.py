import unittest
from maze import Maze

class Tests(unittest.TestCase):
    
    def test_maze_create(self):
        num_cols = 10
        num_rows = 10
        m1 = Maze(num_rows, num_cols, 25)
        self.assertEqual(
            len(m1._cells),
            num_cols * num_rows,
        )
      
    def test_maze_openings(self):
        m2 = Maze(10, 10, 25)
        self.assertEqual(
            m2._cells[0].tw,
            False,
        )
        self.assertEqual(
            m2._cells[-1].bw,
            False,
        )

    def test_maze_reset(self):
        m3 = Maze(10, 10, 25)
        
        for cell in m3._cells:
            cell.visited = True
        
        m3._reset()
        
        for cell in m3._cells:
            self.assertEqual(
                cell.visited,
                False,
            )

if __name__ == "__main__":
    unittest.main()