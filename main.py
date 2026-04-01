from matplotlib.axes import Axes
from typing import Optional
import json
from pathlib import Path
import matplotlib.pyplot as plt

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

def main():
    # exemplificação do uso básico da cifra
    plain_text="Cifra legal e legível"
    cipher="batata"
    print(f"plaintext: {plain_text}")
    print(f"cifra: {cipher}")
    print(f"cipher text: {vigenere_cipher(plain_text, cipher)}")

    # exemplificação da reversibilidade da cifra
    print(vigenere_cipher(vigenere_cipher("Cifrar duas vezes equivale a não fazer nada", 'ab'), 'ab').decode('utf-8'))
    
    sample = get_nth_data_sample(0)
    axes: Axes = plt.subplots(2, 1)[1]
    make_letter_distribuition_panel(sample.plaintext.encode('utf-8'), axes[0], "plaintext")
    make_letter_distribuition_panel(sample.cipher_text, axes[1], "ciphertext")
    plt.show()


if __name__ == "__main__":
    main()
