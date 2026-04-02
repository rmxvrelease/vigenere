from math import sqrt
from matplotlib.axes import Axes
from typing import Optional, Iterable
import json
from pathlib import Path
import matplotlib.pyplot as plt
from numpy import std
J_UTF8_VALUE = 106

class TrainingSample:
    def __init__(self, plaintext: str, comment: Optional[str], language: str, cipher_key: str, cipher_text: bytes):
        self.plaintext:str=plaintext
        self.comment:Optional[str]=comment
        self.language:str=language
        self.cipher_key:str=cipher_key
        self.cipher_text:bytes=cipher_text

    
def vigenere_cipher(
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


def letter_distribuition(text: bytes | str) -> dict[int, int]:
    text_data = (text.encode("utf-8") if isinstance(text, str) else text)
    frequency_dict: dict = {}
    for byte in text_data:
        frequency_dict[byte] = frequency_dict.get(byte, 0) + 1
    return frequency_dict


def make_letter_distribuition_panel(text: bytes, ax: Axes, title: Optional[str]=None):
    ax.hist([b for b in text], bins=256)
    if title:
        ax.set_title(title)


def bytes_multiple_of(n: int, text: bytes) -> bytes:
    return bytes([b for i, b in enumerate(text) if i%n==0])



def get_nth_data_sample(n: int) -> TrainingSample:
    data_path = Path(__file__).parent / 'training_data.json'
    with open(data_path, 'rb') as f:
        sample_file_data = json.load(f)
        plain_text = sample_file_data[n].get("plaintext")
        cipher_key = sample_file_data[n].get("cipher_key")
        cipher_text = vigenere_cipher(plain_text, cipher_key)
        return TrainingSample(
            plain_text,
            sample_file_data[n].get("comment"),
            sample_file_data[n].get("language"),
            cipher_key,
            cipher_text=cipher_text
        )

def standard_deviation(data: str | Iterable[int]) -> int | float:
    if isinstance(data, str):
        data_as_byte_list = [i for i in data.encode('utf-8')]
    elif type(data) is list[int]:
        data_as_byte_list = list(data)
    else:
        data_as_byte_list = [i for i in data]
    avg = sum(i for i in data_as_byte_list)/len(data_as_byte_list)
    return sqrt(sum((i-avg)**2 for i in data_as_byte_list)/len(data_as_byte_list))
    

def main():
    # exemplificação do uso básico da cifra
    plain_text="Cifra legal e legível"
    cipher="batata"
    print(f"plaintext: {plain_text}")
    print(f"cifra: {cipher}")
    print(f"cipher text: {vigenere_cipher(plain_text, cipher)}")

    # exemplificação da reversibilidade da cifra
    print(
        vigenere_cipher(vigenere_cipher("Cifrar duas vezes equivale a não fazer nada", 'ab'), 'ab').decode('utf-8')
    )
    
    sample = get_nth_data_sample(0)
    axes: Axes = plt.subplots(2, 3)[1]
    plt.tight_layout()

    plain_text = sample.plaintext.encode('utf-8')
    plain_text_deviation = std(list(letter_distribuition(plain_text).values()))
    make_letter_distribuition_panel(plain_text, axes[0, 0], title=f"plaintext sd={plain_text_deviation:.4}")

    cipher_text = sample.cipher_text
    cipher_text_deviation = std(list(letter_distribuition(cipher_text).values()))
    make_letter_distribuition_panel(cipher_text, axes[1, 0], title=f"ciphertext sd={cipher_text_deviation:.4}")

    right_multiplicity_plaintext = bytes(list(map(lambda x: x ^ J_UTF8_VALUE, bytes_multiple_of(7, sample.cipher_text))))
    right_multiplicity_plaintext_deviation =std(list(letter_distribuition(right_multiplicity_plaintext).values()))
    make_letter_distribuition_panel(right_multiplicity_plaintext, axes[0, 1], f"multiplicidade certa (plaintext) sd={right_multiplicity_plaintext_deviation:.4}")

    right_multiplicity_ciphertext = bytes_multiple_of(7, sample.cipher_text)
    right_multiplicity_ciphertext_deviation = std(list(letter_distribuition(right_multiplicity_ciphertext).values()))
    make_letter_distribuition_panel(right_multiplicity_ciphertext, axes[1, 1], f"multiplicidade certa (ciphertext) sd={right_multiplicity_ciphertext_deviation:.4}")

    wrong_multiplicity_plain_text = bytes_multiple_of(3, sample.plaintext.encode('utf-8'))
    wrong_multiplicity_plain_text_deviation = std(list(letter_distribuition(wrong_multiplicity_plain_text).values()))
    make_letter_distribuition_panel(wrong_multiplicity_plain_text, axes[0, 2], title=f"multiplicidade errada (plaintext) sd={wrong_multiplicity_plain_text_deviation:.4}")

    wrong_multiplicity_ciphertext = bytes_multiple_of(3, sample.cipher_text)
    wrong_multiplicity_ciphertext_deviation = std(list(letter_distribuition(wrong_multiplicity_ciphertext).values()))
    make_letter_distribuition_panel(wrong_multiplicity_ciphertext, axes[1, 2], f"mutiplicidade errada (ciphertext) sd={wrong_multiplicity_ciphertext_deviation:.4}")


    plt.show()


if __name__ == "__main__":
    main()
