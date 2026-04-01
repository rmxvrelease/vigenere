from typing import Optional
import json
from pathlib import Path
import matplotlib.pyplot as plt

class TrainingSample:
    def __init__(self, plaintext: str, comment: Optional[str], language: str, cipher_key: str):
        self.plaintext=plaintext
        self.comment=comment
        self.language=language
        self.cipher_key=cipher_key

    
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


def letter_distribuition(text: bytes | str) -> dict[int, int]:
    text_data = (text.encode("utf-8") if isinstance(text, str) else text)
    frequency_dict: dict = {}
    for byte in text_data:
        frequency_dict[byte] = frequency_dict.get(byte, 0) + 1
    return frequency_dict


def show_letter_distribuition(text: bytes):
    plt.hist(text, 256)
    plt.show()



def get_nth_data_sample(n: int) -> TrainingSample:
    data_path = Path(__file__).parent / 'training_data.json'
    with open(data_path, 'rb') as f:
        sample_file_data = json.load(f)
        return TrainingSample(
            sample_file_data[n].get("plaintext"),
            sample_file_data[n].get("comment"),
            sample_file_data[n].get("language"),
            sample_file_data[n].get("cipher_key")
        )

def main():
    print(vigenere_cipher(vigenere_cipher("Cifrar duas vezes equivale a não fazer nada", 'ab'), 'ab'))
    print(get_nth_data_sample(0).plaintext)


if __name__ == "__main__":
    main()
