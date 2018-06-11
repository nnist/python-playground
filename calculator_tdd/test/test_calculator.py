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

if __name__ == '__main__':
    unittest.main()
