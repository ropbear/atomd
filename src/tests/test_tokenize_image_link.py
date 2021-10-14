from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [
    (
        b"![image.png](file:///image.png)",
        "{0}image.png{1}file:///image.png{2}"\
            .format(
                LEXICON["image_link_start"].decode('utf-8'),
                LEXICON["image_link_middle"].decode('utf-8'),
                LEXICON["image_link_end"].decode('utf-8')
            )
    ),
    (
        b"![](file:///image.png)",
        "{0}{1}file:///image.png{2}"\
            .format(
                LEXICON["image_link_start"].decode('utf-8'),
                LEXICON["image_link_middle"].decode('utf-8'),
                LEXICON["image_link_end"].decode('utf-8')
            )
    ),
    (
        b"![]()",
        "{0}{1}{2}"\
            .format(
                LEXICON["image_link_start"].decode('utf-8'),
                LEXICON["image_link_middle"].decode('utf-8'),
                LEXICON["image_link_end"].decode('utf-8')
            )
    ),
    (
        b"!()",
        b"!()",
    ),
    (
        b"![]",
        b"![]",
    ),
    (
        b"![](",
        b"![](",
    ),
    (
        b"![] ()",
        b"![] ()",
    ),
    (
        b"! [] ()",
        b"! [] ()",
    ),
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_image_link(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_image_link(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected