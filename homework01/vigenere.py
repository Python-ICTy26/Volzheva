import caesar


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    while len(keyword) < len(plaintext):
        keyword += keyword
    for i in range(0, len(plaintext)):
        shift = ord(keyword[i].lower()) - ord("a")
        ciphertext += caesar.encrypt_caesar(plaintext[i], shift)

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    num_letters = 26
    while len(keyword) < len(ciphertext):
        keyword += keyword
    for i in range(0, len(ciphertext)):
        shift = ord(keyword[i].lower()) - ord("a")
        plaintext += caesar.decrypt_caesar(ciphertext[i], shift)
    return plaintext
