import matplotlib.pyplot as plt

def vigenere_cipher(
    plain_text: str | bytes,
    key: str,
) -> bytes:
    key_extension_factor = len(plain_text) // len(key) + 1
    extended_key_bytes = (key * key_extension_factor).encode('utf-8')
    plain_text_bytes = plain_text.encode('utf-8') if isinstance(plain_text, str) else plain_text
    cipher_text_bytes: list[int] = []
    for (plain_text_byte, key_byte) in zip(plain_text_bytes, extended_key_bytes):
        print(plain_text_byte, key_byte, key_byte ^ plain_text_byte)
        cipher_text_bytes.append(plain_text_byte ^ key_byte)
    return bytes(cipher_text_bytes)


def letter_distribuition():
    ...


def main():
    print(vigenere_cipher(vigenere_cipher("Cifrar duas vezes equivale a não fazer nada", 'ab'), 'ab'))


if __name__ == "__main__":
    main()
