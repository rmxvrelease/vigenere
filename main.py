from matplotlib.axes import Axes
from typing import Optional
import json
from pathlib import Path
import matplotlib.pyplot as plt
from numpy import std
import string

J_UTF8_VALUE = 106

DECODE_LETTER_TABLE: dict[int, str] = {i: v for i, v in enumerate(string.ascii_lowercase + ' ')}
ENCODE_LETTER_TABLE: dict[str, int] = {v: i for i, v in enumerate(string.ascii_lowercase + ' ')}
ENGLISH_ALPHABET_SIZE = len(ENCODE_LETTER_TABLE)

class TrainingSample:
    def __init__(self, plaintext: str, comment: Optional[str], language: str, cipher_key: str, cipher_text: bytes):
        self.plaintext:str=plaintext
        self.comment:Optional[str]=comment
        self.language:str=language
        self.cipher_key:str=cipher_key
        self.cipher_text:bytes=cipher_text

    
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
    plain_text_lower_case: str = plain_text.lower()
    cipher_text = ""
    for i, c in enumerate(plain_text_lower_case):
        key_char_num = ENCODE_LETTER_TABLE[key[i%len(key)]]
        plain_char_num = ENCODE_LETTER_TABLE[c]
        cyphertext_char = DECODE_LETTER_TABLE[(key_char_num+plain_char_num)%ENGLISH_ALPHABET_SIZE]
        cipher_text += cyphertext_char

def vigenere_cipher_decode_english_letters(cipher_text: str, key: str):
    plain_text_lower_case: str = cipher_text.lower()
    cipher_text = ""
    for i, c in enumerate(plain_text_lower_case):
        key_char_num = ENCODE_LETTER_TABLE[key[i%len(key)]]
        plain_char_num = ENCODE_LETTER_TABLE[c]
        cyphertext_char = DECODE_LETTER_TABLE[(key_char_num-plain_char_num)%ENGLISH_ALPHABET_SIZE]
        cipher_text += cyphertext_char
    return cipher_text

def byte_distribuition(text: bytes | str) -> dict[int, int]:
    text_data = (text.encode("utf-8") if isinstance(text, str) else text)
    frequency_dict: dict = {i: 0 for i in range(256)}
    for byte in text_data:
        frequency_dict[byte] = frequency_dict.get(byte, 0) + 1
    return {k: v/len(text_data) for (k,v) in frequency_dict.items()}

def letter_distribuition(text: str) -> dict[str, int]:
    frequency_dict: dict = {i: 0 for i in string.ascii_lowercase+' '}
    for letter in text:
        frequency_dict[letter]+=1
    return {k: v/len(text) for (k,v) in frequency_dict.items()}


def make_byte_distribuition_panel(text: bytes, ax: Axes, title: Optional[str]=None):
    ax.hist([b for b in text], bins=256)
    if title:
        ax.set_title(title)

# def make_letter_distribuition_panel(text: str, ax: Axes, title: Optional[str]=None):
#     ax.hist([c for c in text], bins=len(ENCODE_LETTER_TABLE))
#     if title:
#         ax.set_title(title)

def bytes_multiple_of(n: int, text: bytes) -> bytes:
    return bytes([b for i, b in enumerate(text) if i%n==0])



def get_nth_data_sample(n: int) -> TrainingSample:
    data_path = Path(__file__).parent / 'training_data.json'
    with open(data_path, 'rb') as f:
        sample_file_data = json.load(f)
        plain_text = sample_file_data[n].get("plaintext")
        cipher_key = sample_file_data[n].get("cipher_key")
        cipher_text = vigenere_cipher_bytes(plain_text, cipher_key)
        return TrainingSample(
            plain_text,
            sample_file_data[n].get("comment"),
            sample_file_data[n].get("language"),
            cipher_key,
            cipher_text=cipher_text
        )


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

def main():
    # exemplificação do uso básico da cifra
    plain_text="Cifra legal e legível"
    cipher="batata"
    print(f"plaintext: {plain_text}")
    print(f"cifra: {cipher}")
    print(f"cipher text: {vigenere_cipher_bytes(plain_text, cipher)}")

    # exemplificação da reversibilidade da cifra
    print(
        vigenere_cipher_bytes(vigenere_cipher_bytes("Cifrar duas vezes equivale a não fazer nada", 'ab'), 'ab').decode('utf-8')
    )
    
    sample = get_nth_data_sample(0)
    axes: Axes = plt.subplots(2, 3)[1]
    plt.tight_layout()

    plain_text = sample.plaintext.encode('utf-8')
    plain_text_deviation = std(list(byte_distribuition(plain_text).values()))
    make_byte_distribuition_panel(plain_text, axes[0, 0], title=f"plaintext sd={plain_text_deviation:.4}")

    cipher_text = sample.cipher_text
    cipher_text_deviation = std(list(byte_distribuition(cipher_text).values()))
    make_byte_distribuition_panel(cipher_text, axes[1, 0], title=f"ciphertext sd={cipher_text_deviation:.4}")

    right_multiplicity_plaintext = bytes(list(map(lambda x: x ^ J_UTF8_VALUE, bytes_multiple_of(7, sample.cipher_text))))
    right_multiplicity_plaintext_deviation =std(list(byte_distribuition(right_multiplicity_plaintext).values()))
    make_byte_distribuition_panel(right_multiplicity_plaintext, axes[0, 1], f"multiplicidade certa (plaintext) sd={right_multiplicity_plaintext_deviation:.4}")

    right_multiplicity_ciphertext = bytes_multiple_of(7, sample.cipher_text)
    right_multiplicity_ciphertext_deviation = std(list(byte_distribuition(right_multiplicity_ciphertext).values()))
    make_byte_distribuition_panel(right_multiplicity_ciphertext, axes[1, 1], f"multiplicidade certa (ciphertext) sd={right_multiplicity_ciphertext_deviation:.4}")

    wrong_multiplicity_plain_text = bytes_multiple_of(3, sample.plaintext.encode('utf-8'))
    wrong_multiplicity_plain_text_deviation = std(list(byte_distribuition(wrong_multiplicity_plain_text).values()))
    make_byte_distribuition_panel(wrong_multiplicity_plain_text, axes[0, 2], title=f"multiplicidade errada (plaintext) sd={wrong_multiplicity_plain_text_deviation:.4}")

    wrong_multiplicity_ciphertext = bytes_multiple_of(3, sample.cipher_text)
    wrong_multiplicity_ciphertext_deviation = std(list(byte_distribuition(wrong_multiplicity_ciphertext).values()))
    make_byte_distribuition_panel(wrong_multiplicity_ciphertext, axes[1, 2], f"mutiplicidade errada (ciphertext) sd={wrong_multiplicity_ciphertext_deviation:.4}")

    print(find_key_size(cipher_text, range(1, 9))) # função que acha o tamanho da chave
    print(break_vigenere(cipher_text, range(1, 9)))

    plt.show()


if __name__ == "__main__":
    main()
