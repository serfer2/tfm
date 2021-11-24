import re
from typing import List

HF_TAGS_PATTERN = r'(?P<tag>\*\*\*\w*\*\*\*)+(.*)(?P=tag)+'
TOKENIZE_SUB_PATTERN = r'[^0-9a-z$€£₽\']'


def hf_clean_text(text: str) -> str:
    _text = text.replace('\n', ' ').replace('\t', ' ')
    _text = re.sub(
        pattern=HF_TAGS_PATTERN,
        repl='',
        string=_text,
    )
    for _ in range(10):
        _text = _text.replace('  ', ' ')
    return _text.strip()


def tokenize(text: str) -> List[str]:
    lower_cleaned_text = re.sub(
        pattern=TOKENIZE_SUB_PATTERN,
        repl=' ',
        string=text.lower(),
    )
    words = [_w.strip() for _w in lower_cleaned_text.split(' ') if _w.strip()]
    # unique words in same order of appearance
    unique_words = []
    for word in words:
        if word in unique_words:
            continue
        unique_words.append(word)

    return unique_words
