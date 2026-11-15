"""шифр Цезаря"""


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    шифрует текст шифром Цезаря

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    >>> encrypt_caesar("ABC", 0)
    'ABC'
    """
    ciphertext = ""

    # сдвигает толькр английские буквы
    for char in plaintext:
        if "A" <= char <= "Z":
            new_char = chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            ciphertext += new_char
        elif "a" <= char <= "z":
            new_char = chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            ciphertext += new_char
        else:
            ciphertext += char

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    расшифровывает текст зашифрованный  Цезарем

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    >>> decrypt_caesar("ABC", 0)
    'ABC'
    """
    plaintext = ""

    # для расшифровки обратный сдвиг
    for char in ciphertext:
        if "A" <= char <= "Z":
            new_char = chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            plaintext += new_char
        elif "a" <= char <= "z":
            new_char = chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
            plaintext += new_char
        else:
            plaintext += char

    return plaintext
