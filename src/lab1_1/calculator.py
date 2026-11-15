def add(first_number: float, second_number: float) -> float:
    """сумму двух чисел"""
    return first_number + second_number


def subtract(first_number: float, second_number: float) -> float:
    """разность двух чисел"""
    return first_number - second_number


def multiply(first_number: float, second_number: float) -> float:
    """произведение двух чисел"""
    return first_number * second_number


def divide(first_number: float, second_number: float) -> float:
    """деление на 0"""
    if second_number == 0:
        raise ZeroDivisionError("Деление на ноль невозможно.")
    return first_number / second_number


def calculate(first_number: float, operator: str, second_number: float) -> float:
    """арифметическая операция, зависит от оператора"""
    if operator == "+":
        return add(first_number, second_number)
    if operator == "-":
        return subtract(first_number, second_number)
    if operator == "*":
        return multiply(first_number, second_number)
    if operator == "/":
        return divide(first_number, second_number)

    raise ValueError(f"Неподдерживаемая операция: {operator}")
