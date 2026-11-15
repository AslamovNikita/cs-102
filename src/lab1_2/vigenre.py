"""шифр Виженера"""


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    шифрует с помощью шифра Виженера

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    >>> encrypt_vigenere("Hello, World!", "KEY")
    'Rijvs, Uyvjn!'
    """
    if not keyword or not keyword.isalpha() or not keyword.isascii():
        raise ValueError("Ключ должен содержать английские буквы.")

    ciphertext = ""
    key_index = 0

    for char in plaintext:
        if "A" <= char <= "Z":
            shift = ord(keyword[key_index % len(keyword)].upper()) - ord("A")
            new_char = chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            ciphertext += new_char
            key_index += 1
        elif "a" <= char <= "z":
            shift = ord(keyword[key_index % len(keyword)].upper()) - ord("A")
            new_char = chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            ciphertext += new_char
            key_index += 1
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    расшифровывает текст зашифрованный  Виженером

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    >>> decrypt_vigenere("Rijvs, Uyvjn!", "KEY")
    'Hello, World!'
    """
    if not keyword or not keyword.isalpha() or not keyword.isascii():
        raise ValueError("Ключ должен содержать английские буквы.")
    plaintext = ""
    key_index = 0

    for char in ciphertext:
        if "A" <= char <= "Z":
            shift = ord(keyword[key_index % len(keyword)].upper()) - ord("A")
            new_char = chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            plaintext += new_char
            key_index += 1
        elif "a" <= char <= "z":
            shift = ord(keyword[key_index % len(keyword)].upper()) - ord("A")
            new_char = chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
            plaintext += new_char
            key_index += 1
        else:
            plaintext += char

    return plaintext
