from matplotlib.axes import Axes
from typing import Optional
from .vigenere import ENCODE_LETTER_TABLE

def make_byte_distribuition_panel(text: bytes, ax: Axes, title: Optional[str]=None):
    ax.hist([b for b in text], bins=256)
    if title:
        ax.set_title(title)

def make_letter_distribuition_panel(text: str, ax: Axes, title: Optional[str]=None):
    ax.hist([c for c in text], bins=len(ENCODE_LETTER_TABLE))
    if title:
        ax.set_title(title)
