from numpy import std
import string

DECODE_LETTER_TABLE: dict[int, str] = {i: v for i, v in enumerate(string.ascii_lowercase + ' ')}
ENCODE_LETTER_TABLE: dict[str, int] = {v: i for i, v in enumerate(string.ascii_lowercase + ' ')}
ENGLISH_ALPHABET_SIZE = len(ENCODE_LETTER_TABLE)

def vigenere_cipher_bytes(
    plain_text: str | bytes,
    key: str,
) -> bytes:
    key_extension_factor = len(plain_text) // len(key) + 1
    extended_key_bytes = (key * key_extension_factor).encode('utf-8')
    plain_text_bytes = plain_text.encode('utf-8') if isinstance(plain_text, str) else plain_text
    cipher_text_bytes: list[int] = []
    for (plain_text_byte, key_byte) in zip(plain_text_bytes, extended_key_bytes):
        cipher_text_bytes.append(plain_text_byte ^ key_byte)
    return bytes(cipher_text_bytes)


def vigenere_cipher_encode_english_letters(plain_text: str, key: str):
    plain_text_lower_case: str = ''.join([c for c in plain_text.lower() if c in string.ascii_lowercase+' '])
    cipher_text = ""
    for i, c in enumerate(plain_text_lower_case):
        key_char_num = ENCODE_LETTER_TABLE[key[i%len(key)]]
        plain_char_num = ENCODE_LETTER_TABLE[c]
        cyphertext_char = DECODE_LETTER_TABLE[(key_char_num+plain_char_num)%ENGLISH_ALPHABET_SIZE]
        cipher_text += cyphertext_char
    return cipher_text


def vigenere_cipher_decode_english_letters(cipher_text: str, key: str):
    cipher_text_lower_case: str = cipher_text.lower()
    plain_text = ""
    for i, c in enumerate(cipher_text_lower_case):
        key_char_num = ENCODE_LETTER_TABLE[key[i%len(key)]]
        cipher_text_char_num = ENCODE_LETTER_TABLE[c]
        plain_text_char = DECODE_LETTER_TABLE[(cipher_text_char_num-key_char_num)%ENGLISH_ALPHABET_SIZE]
        plain_text += plain_text_char
    return plain_text


def bytes_multiple_of(n: int, text: bytes) -> bytes:
    return bytes([b for i, b in enumerate(text) if i%n==0])


def letters_multiple_of(n: int, text: str) -> str: 
    return ''.join([b for i, b in enumerate(text) if i%n==0])


def byte_distribuition(text: bytes | str) -> dict[int, int]:
    text_data = (text.encode("utf-8") if isinstance(text, str) else text)
    frequency_dict: dict = {i: 0 for i in range(256)}
    for byte in text_data:
        frequency_dict[byte] = frequency_dict.get(byte, 0) + 1
    return {k: v/len(text_data) for (k,v) in frequency_dict.items()}


def letter_distribuition(text: str) -> dict[str, int]:
    text = text.lower()
    frequency_dict: dict = {i: 0 for i in string.ascii_lowercase+' '}
    for letter in text:
        if letter not in string.ascii_lowercase + ' ':
            continue
        frequency_dict[letter]+=1
    return {k: v/len(text) for (k,v) in frequency_dict.items()}


def find_key_size(ciphertext: bytes, test_range: range) -> int:
    test_results: list[tuple[int, int|float]] = []
    for size_tested in test_range:
        cipher_sample = bytes_multiple_of(size_tested, ciphertext)
        deviation = std(list(byte_distribuition(cipher_sample).values()))
        test_results.append((size_tested, deviation))
    return max(test_results, key=lambda a: a[1])[0]   


def break_vigenere(ciphertext: bytes, key_range: range) -> tuple[str, str]:
    key_size = find_key_size(ciphertext, key_range)    
    recovered_key_bytes = []
    for i in range(key_size):
        slice_bytes = bytes_multiple_of(key_size, ciphertext[i:])
        best_byte = 0
        max_score = -1
        for candidate_byte in range(256):
            decrypted_slice = bytes([b ^ candidate_byte for b in slice_bytes])
            current_score = 0
            for b in decrypted_slice:
                if b == 32:
                    current_score += 5
                elif 97 <= b <= 122:
                    current_score += 2
                elif 65 <= b <= 90:
                    current_score += 1
                elif 48 <= b <= 57:
                    current_score += 1
                elif b > 127:
                    current_score -= 10
            if current_score > max_score:
                max_score = current_score
                best_byte = candidate_byte        
        recovered_key_bytes.append(best_byte)
    key = bytes(recovered_key_bytes).decode('utf-8', errors='replace')
    decrypted_bytes = vigenere_cipher_bytes(ciphertext, key)    
    return key, decrypted_bytes.decode('utf-8', errors='replace')
