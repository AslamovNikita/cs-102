"""Тесты для шифра Виженера"""
import pytest
from src.lab1_2.vigenre import decrypt_vigenere, encrypt_vigenere

@pytest.mark.parametrize(
    ("plaintext", "keyword", "expected"),
    [
        ("PYTHON", "A", "PYTHON"),
        ("python", "a", "python"),
        ("ATTACKATDAWN", "LEMON", "LXFOPVEFRNHR"),
        ("Hello, World!", "KEY", "Rijvs, Uyvjn!"),
        ("A!A", "BC", "B!C"),
        ("AЖA", "BC", "BЖC"),
    ],
)
def test_encrypt_vigenere(plaintext, keyword, expected):
    """Проверка шифрования"""
    assert encrypt_vigenere(plaintext, keyword) == expected

@pytest.mark.parametrize(
    ("ciphertext", "keyword", "expected"),
    [
        ("PYTHON", "A", "PYTHON"),
        ("python", "a", "python"),
        ("LXFOPVEFRNHR", "LEMON", "ATTACKATDAWN"),
        ("Rijvs, Uyvjn!", "KEY", "Hello, World!"),
        ("B!C", "BC", "A!A"),
        ("BЖC", "BC", "AЖA"),
    ],
)
def test_decrypt_vigenere(ciphertext, keyword, expected):
    """Проверка расшифровки"""
    assert decrypt_vigenere(ciphertext, keyword) == expected

@pytest.mark.parametrize(
    "keyword",
    [
        "",
        "KEY1",
        "KEY!",
        "КЛЮЧ",
        "Ä",
    ],
)
def test_invalid_keyword(keyword):
    """Проверка неправильного ключа"""
    with pytest.raises(ValueError):
        encrypt_vigenere("HELLO", keyword)
    with pytest.raises(ValueError):
        decrypt_vigenere("HELLO", keyword)

def test_vigenere_empty_string():
    """Обработки пустой строки"""
    assert encrypt_vigenere("", "KEY") == ""
    assert decrypt_vigenere("", "KEY") == ""

def test_vigenere_round_trip():
    """Проверка обратимости шифрования"""
    plaintext = "Hello, World! ATTACK AT DAWN"
    encrypted = encrypt_vigenere(plaintext, "LEMON")
    decrypted = decrypt_vigenere(encrypted, "LEMON")
    assert decrypted == plaintext