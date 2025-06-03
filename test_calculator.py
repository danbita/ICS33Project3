import unittest
from grin.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_ints(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_add_floats(self):
        self.assertEqual(self.calc.add(2.5, 3.5), 6.0)

    def test_add_int_and_float(self):
        self.assertEqual(self.calc.add(2, 3.5), 5.5)
        self.assertEqual(self.calc.add(2.5, 3), 5.5)

    def test_add_strings(self):
        self.assertEqual(self.calc.add('Dan ', 'Bita'), 'Dan Bita')

    def test_invalid_addition(self):
        with self.assertRaises(ValueError):
            self.calc.add(2, 'Dan')

    def test_subtract_ints(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_subtract_floats(self):
        self.assertEqual(self.calc.subtract(5.5, 3.0), 2.5)

    def test_subtract_int_and_float(self):
        self.assertEqual(self.calc.subtract(5, 2.5), 2.5)
        self.assertEqual(self.calc.subtract(5.5, 2), 3.5)

    def test_subtract_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.subtract('Dan', 2)

    def test_multiply_ints(self):
        self.assertEqual(self.calc.multiply(4, 3), 12)

    def test_multiply_floats(self):
        self.assertEqual(self.calc.multiply(2.5, 2.0), 5.0)

    def test_multiply_int_and_float(self):
        self.assertEqual(self.calc.multiply(4, 2.5), 10.0)
        self.assertEqual(self.calc.multiply(2.5, 4), 10.0)

    def test_multiply_string_and_int(self):
        self.assertEqual(self.calc.multiply('dan', 3), 'dandandan')
        self.assertEqual(self.calc.multiply(3, 'bita'), 'bitabitabita')

    def test_multiply_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.multiply('dan', 2.5)

    def test_divide_ints(self):
        self.assertEqual(self.calc.divide(8, 2), 4)

    def test_divide_floats(self):
        self.assertEqual(self.calc.divide(7.5, 2.5), 3.0)

    def test_divide_int_and_float(self):
        self.assertEqual(self.calc.divide(8, 2.0), 4.0)
        self.assertEqual(self.calc.divide(8.0, 2), 4.0)

    def test_divide_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.divide('dan', 2)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(5, 0)

if __name__ == '__main__':
    unittest.main()