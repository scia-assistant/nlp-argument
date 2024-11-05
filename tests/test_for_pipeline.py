import unittest


class TestPipeline(unittest.TestCase):

    def test_addition(self):
        """A simple test for addition"""
        self.assertEqual(1 + 1, 2)

    def test_subtraction(self):
        """A simple test for subtraction"""
        self.assertEqual(5 - 3, 2)

    def test_multiplication(self):
        """A simple test for multiplication"""
        self.assertEqual(3 * 3, 9)

    def test_division(self):
        """A simple test for division"""
        self.assertEqual(10 / 2, 5)


if __name__ == '__main__':
    unittest.main()
