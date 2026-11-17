"""Тесты для шифра Цезаря"""
import pytest
from src.lab1_2.caesar import decrypt_caesar, encrypt_caesar

@pytest.mark.parametrize(
    ("plaintext", "shift", "expected"),
    [
        ("PYTHON", 3, "SBWKRQ"),
        ("python", 3, "sbwkrq"),
        ("Python3.6", 3, "Sbwkrq3.6"),
        ("ABC", 0, "ABC"),
        ("ABC", -1, "ZAB"),
        ("ABC", 29, "DEF"),
    ],
)
def test_encrypt_caesar(plaintext, shift, expected):
    """Проверка шифрования"""
    assert encrypt_caesar(plaintext, shift) == expected

def test_encrypt_caesar_preserves_symbols():
    """Проверка сохранения знаков цифр и русских букв"""
    assert encrypt_caesar("Hello, Мир! 123") == "Khoor, Мир! 123"

@pytest.mark.parametrize(
    ("ciphertext", "shift", "expected"),
    [
        ("SBWKRQ", 3, "PYTHON"),
        ("sbwkrq", 3, "python"),
        ("Sbwkrq3.6", 3, "Python3.6"),
        ("ABC", 0, "ABC"),
        ("ZAB", -1, "ABC"),
    ],
)
def test_decrypt_caesar(ciphertext, shift, expected):
    """Проверка расшифровки"""
    assert decrypt_caesar(ciphertext, shift) == expected

def test_caesar_empty_string():
    """Обработки пустой строки"""
    assert encrypt_caesar("") == ""
    assert decrypt_caesar("") == ""

def test_caesar_round_trip():
    """Проверка обратимости шифрованя"""
    plaintext = "Hello, Python! 123"
    encrypted = encrypt_caesar(plaintext)
    decrypted = decrypt_caesar(encrypted)
    assert decrypted == plaintext