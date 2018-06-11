import unittest
from app.calculator import Calculator

class CalculatorTest(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_calculator_add_method_returns_correct_result(self):
        result = self.calc.add(2, 2)
        self.assertEqual(4, result)

    def test_calculator_add_method_raise_error_on_wrong_input(self):
        self.assertRaises(ValueError, self.calc.add, 'two', 'three')
        self.assertRaises(ValueError, self.calc.add, 1, 'a')

    def test_calculator_subtract_method_returns_correct_result(self):
        result = self.calc.subtract(4, 1)
        self.assertEqual(3, result)

    def test_calculator_subtract_method_raise_error_on_wrong_input(self):
        self.assertRaises(ValueError, self.calc.subtract, 'two', 'three')
        self.assertRaises(ValueError, self.calc.subtract, 1, 'a')

    def test_calculator_multiply_method_returns_correct_result(self):
        result = self.calc.multiply(3, 4)
        self.assertEqual(12, result)

    def test_calculator_multiply_method_raise_error_on_wrong_input(self):
        self.assertRaises(ValueError, self.calc.multiply, 'two', 'three')
        self.assertRaises(ValueError, self.calc.multiply, 1, 'a')

    def test_calculator_divide_method_returns_correct_result(self):
        result = self.calc.divide(15, 5)
        self.assertEqual(3, result)

    def test_calculator_divide_method_raise_error_on_wrong_input(self):
        self.assertRaises(ValueError, self.calc.divide, 'two', 'three')
        self.assertRaises(ValueError, self.calc.divide, 1, 'a')

    def test_calculator_divide_method_raise_error_on_divide_by_zero(self):
        self.assertRaises(ZeroDivisionError, self.calc.divide, 16, 0)

    def test_calculator_power_method_returns_correct_result(self):
        result = self.calc.power(5, 3)
        self.assertEqual(125, result)

    def test_calculator_power_method_raise_error_on_wrong_input(self):
        self.assertRaises(ValueError, self.calc.power, 'two', 'three')
        self.assertRaises(ValueError, self.calc.power, 1, 'a')

    def test_calculator_root_method_returns_correct_result(self):
        result = self.calc.root(16, 2)
        self.assertEqual(4, result)
        result = self.calc.root(8, 3)
        self.assertEqual(2, result)

    def test_calculator_root_method_raise_error_on_wrong_input(self):
        self.assertRaises(ValueError, self.calc.root, 'two', 'three')
        self.assertRaises(ValueError, self.calc.root, 1, 'a')

if __name__ == '__main__':
    unittest.main()
