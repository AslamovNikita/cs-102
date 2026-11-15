"""тесты"""
import unittest

from src.lab1_1.calculator import (
    add,
    calculate,
    divide,
    multiply,
    subtract,
)

class CalculatorTestCase(unittest.TestCase):
    """проверка основных операций"""

    def test_add(self):
        """сложение"""
        self.assertEqual(add(10, 5), 15)

    def test_subtract(self):
        """вычитание"""
        self.assertEqual(subtract(10, 5), 5)

    def test_multiply(self):
        """умножение"""
        self.assertEqual(multiply(10, 5), 50)

    def test_divide(self):
        """деление"""
        self.assertEqual(divide(10, 5), 2)

    def test_divide_by_zero(self):
        """проверяет деление на ноль"""
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_calculate_add(self):
        """проверяет сложение через общую функцию"""
        self.assertEqual(calculate(10, "+", 5), 15)

    def test_calculate_subtract(self):
        """вычитание через общую функцию"""
        self.assertEqual(calculate(10, "-", 5), 5)

    def test_calculate_multiply(self):
        """умножение через общую функцию"""
        self.assertEqual(calculate(10, "*", 5), 50)

    def test_calculate_divide(self):
        """деление через общую функцию"""
        self.assertEqual(calculate(10, "/", 5), 2)

    def test_invalid_operator(self):
        """обработка неизвестной операции"""
        with self.assertRaises(ValueError):
            calculate(10, "%", 5)

if __name__ == "__main__":
    unittest.main()
