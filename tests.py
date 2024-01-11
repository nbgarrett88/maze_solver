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
        num_cols = 10
        num_rows = 10
        m2 = Maze(num_rows, num_cols, 25)
        self.assertEqual(
            m2._cells[0].tw,
            False,
        )
        self.assertEqual(
            m2._cells[-1].bw,
            False,
        )

if __name__ == "__main__":
    unittest.main()