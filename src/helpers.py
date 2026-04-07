from typing import Optional
from pathlib import Path
from . import vigenere
import json

class TrainingSample:
    def __init__(self, plaintext: str, comment: Optional[str], language: str, cipher_key: str, cipher_text: bytes):
        self.plaintext:str=plaintext
        self.comment:Optional[str]=comment
        self.language:str=language
        self.cipher_key:str=cipher_key
        self.cipher_text:bytes=cipher_text

def get_nth_data_sample(n: int) -> TrainingSample:
    data_path = Path(__file__).parent.parent / 'training_data.json'
    with open(data_path, 'rb') as f:
        sample_file_data = json.load(f)
        plain_text = sample_file_data[n].get("plaintext")
        cipher_key = sample_file_data[n].get("cipher_key")
        cipher_text = vigenere.vigenere_cipher_bytes(plain_text, cipher_key)
        return TrainingSample(
            plain_text,
            sample_file_data[n].get("comment"),
            sample_file_data[n].get("language"),
            cipher_key,
            cipher_text=cipher_text
        )
