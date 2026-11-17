"""Тесты для RSA"""
import pytest
from src.lab1_2 import rsa
@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (-5, False),
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (8, False),
        (9, False),
        (17, True),
        (19, True),
    ],
)
def test_is_prime(number, expected):
    """Проверка определения простых чисел"""
    assert rsa.is_prime(number) is expected

@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (12, 15, 3),
        (3, 7, 1),
        (-12, 15, 3),
        (0, 5, 5),
        (0, 0, 0),
    ],
)
def test_gcd(a, b, expected):
    """Проверка нахождения НОД"""
    assert rsa.gcd(a, b) == expected

def test_multiplicative_inverse():
    """Проверка поиска обратного элемент"""
    assert rsa.multiplicative_inverse(7, 40) == 23

def test_multiplicative_inverse_invalid():
    """Проверка когда обратного элемента нет"""
    with pytest.raises(ValueError):
        rsa.multiplicative_inverse(6, 40)

def test_generate_keypair(monkeypatch):
    """Проверка генерации ключей"""
    def fixed_exponent(_start, _stop):
        return 5
    monkeypatch.setattr(rsa.random, "randrange", fixed_exponent)
    public_key, private_key = rsa.generate_keypair(17, 19)
    assert public_key == (5, 323)
    assert private_key == (173, 323)

@pytest.mark.parametrize(
    ("p", "q"),
    [
        (4, 7),
        (7, 4),
        (17, 17),
    ],
)
def test_generate_keypair_invalid(p, q):
    """Проверка неправильных исходных чисел"""
    with pytest.raises(ValueError):
        rsa.generate_keypair(p, q)


def test_rsa_encrypt_decrypt():
    """Шифрование и расшифровка сообщения"""
    public_key = (5, 323)
    private_key = (173, 323)
    plaintext = "HELLO 123"
    ciphertext = rsa.encrypt(public_key, plaintext)
    decrypted = rsa.decrypt(private_key, ciphertext)
    assert decrypted == plaintext

def test_rsa_reverse_encrypt_decrypt():
    """Проверка шифрования закрытым, расшифровки открытым ключоми"""
    public_key = (5, 323)
    private_key = (173, 323)
    plaintext = "PYTHON"
    ciphertext = rsa.encrypt(private_key, plaintext)
    decrypted = rsa.decrypt(public_key, ciphertext)
    assert decrypted == plaintext

def test_rsa_empty_string():
    """Проверка пустого сообщения"""
    ciphertext = rsa.encrypt((5, 323), "")
    assert ciphertext == []
    assert rsa.decrypt((173, 323), ciphertext) == ""