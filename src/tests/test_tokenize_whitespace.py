from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [
    (
        b" ",
        LEXICON["space"]
    ),
    (
        b"\t",
        LEXICON["horizontal_tab"]
    ),
    (
        b"\n",
        LEXICON["newline"]
    ),
    (
        b" \n\t\n ",
        "{0}{1}{2}{1}{0}"\
            .format(
                LEXICON["space"].decode('utf-8'),
                LEXICON["newline"].decode('utf-8'),
                LEXICON["horizontal_tab"].decode('utf-8')
            )
    )
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_whitespace(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_whitespace(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected