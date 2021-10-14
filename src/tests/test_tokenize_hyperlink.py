from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [
    (
        b"[google](https://google.com)",
        "{0}google{1}https://google.com{2}"\
            .format(
                LEXICON["link_start"].decode('utf-8'),
                LEXICON["link_middle"].decode('utf-8'),
                LEXICON["link_end"].decode('utf-8')
            )
    ),
    (
        b"[](https://google.com)",
        "{0}{1}https://google.com{2}"\
            .format(
                LEXICON["link_start"].decode('utf-8'),
                LEXICON["link_middle"].decode('utf-8'),
                LEXICON["link_end"].decode('utf-8')
            )
    ),
    (
        b"[]()",
        "{0}{1}{2}"\
            .format(
                LEXICON["link_start"].decode('utf-8'),
                LEXICON["link_middle"].decode('utf-8'),
                LEXICON["link_end"].decode('utf-8')
            )
    ),
    (
        b"()",
        b"()",
    ),
    (
        b"[]",
        b"[]",
    ),
    (
        b"[](",
        b"[](",
    ),
    (
        b"[] ()",
        b"[] ()",
    ),
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_hyperlink(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_hyperlink(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected