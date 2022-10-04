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
    num_letters = 26
    while len(keyword) < len(plaintext):
        keyword += keyword
    for i in range(0, len(plaintext)):
        if plaintext[i] in alfavit:
            shift = ord(keyword[i].lower()) - ord('a')
            if plaintext[i].lower() == plaintext[i]:
                start = ord('a')
            else:
                start = ord('A')
            ciphertext += chr(start + (ord(plaintext[i]) + shift - start) % num_letters)
        else:
            ciphertext += plaintext[i]
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
        if ciphertext[i] in alfavit:
            shift = ord(keyword[i].lower()) - ord('a')
            if ciphertext[i].lower() == ciphertext[i]:
                start = ord('a')
            else:
                start = ord('A')
            plaintext += chr(start + (ord(ciphertext[i]) - shift - start) % num_letters)
        else:
            plaintext += ciphertext[i]
    return plaintext
