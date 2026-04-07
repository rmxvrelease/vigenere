from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from numpy import std
from src.vigenere import (
    byte_distribuition,
    vigenere_cipher_bytes,
    bytes_multiple_of,
    vigenere_cipher_decode_english_letters,
    vigenere_cipher_encode_english_letters,
    find_key_size,
    break_vigenere,
    letter_distribuition
)
from src.helpers import get_nth_data_sample
from src.display import make_byte_distribuition_panel, make_letter_distribuition_panel

J_UTF8_VALUE = 106

def letter_vigenere_demo():
    plain_text="Cifra legal e legivel"
    key='ab'
    cipher_text = vigenere_cipher_encode_english_letters(plain_text, key)
    decoded_cipher_text = vigenere_cipher_decode_english_letters(cipher_text, key)
    print(f"plain_text: {plain_text}")
    print(f"key: {key}")
    print(f"cipher_text: {cipher_text}")
    print(f"decoded_cipher_text: {decoded_cipher_text}")


def letter_distribuition_demo():
    plain_text="""
        Here is how to break the vigenere cipher.
        First, we begin by assuming a sufficiently long plaintext. For our purposes, sufficiently long means any text that approaches
        the averege language letter distribuition. With the plain text in hands, we then apply the vigenere cipher to it using a relatively short key,
        obtaining the ciphertext. The next step to break the vigenere cipher is trying to find the lenght of the key that generated our ciphertext.
        To acomplish this goal, the standard procedure is to test each possible key size 'n', selecting from the ciphertext the letters whose position is
        multiple of 'n'...
        """
    ciphertext = vigenere_cipher_encode_english_letters(plain_text, 'let')
    print(f'plain_text: {plain_text}')
    print(f'cipher_text: {ciphertext}')
    print(letter_distribuition(plain_text))
    fig, axes = plt.subplots(1, 2)
    plt.tight_layout()
    make_letter_distribuition_panel(ciphertext, axes[0], 'letter dist')
    make_letter_distribuition_panel(plain_text, axes[1], 'letter dist')
    plt.show()


def normal_show():
    plain_text="Cifra legal e legível"
    cipher="batata"
    print(f"\033[32mplaintext\033[0m: {plain_text}")
    print(f"\033[32mcifra\033[0m: {cipher}")
    print(f"\033[32mcipher text\033[0m: {vigenere_cipher_bytes(plain_text, cipher)}")

    # exemplificação da reversibilidade da cifra
    print(f'\033[32mobs\033[0m: {
        vigenere_cipher_bytes(vigenere_cipher_bytes("Cifrar duas vezes equivale a não fazer nada", 'ab'), 'ab').decode('utf-8')}\033[0m'
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

    print(f'\033[32mkey\033[0m: {sample.cipher_key}')
    print(f'\033[32mplain_text\033[0m: {sample.plaintext[:50]}')
    print(f'\033[32mcipher_text\033[0m: {sample.cipher_text[:50]}')

    print(f"\033[32mkey_size\033[0m: {find_key_size(cipher_text, range(1, 9))}") # função que acha o tamanho da chave
    print(f"\033[32mreconstructed_text\033[0m: {break_vigenere(cipher_text, range(1, 9))[:50]}")

    plt.show()

if __name__ == "__main__":
    normal_show()
