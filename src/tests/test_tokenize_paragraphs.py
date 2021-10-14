from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [
    (
        b"\n this is a random block of text \n",
        "{0} this is a random block of text {1}"\
            .format(
                LEXICON["paragraph_start"].decode('utf-8'),
                LEXICON["paragraph_end"].decode('utf-8')
            )
    ),
    (
        b"\n this is a random \nblock of text \n",
        "{0} this is a random {1}\n{0}block of text {1}"\
            .format(
                LEXICON["paragraph_start"].decode('utf-8'),
                LEXICON["paragraph_end"].decode('utf-8')
            )
    ),
    (
        b"\n{{italic_start}}this is a random block of text {{italic_end}}\n",
        "{0}{{{{italic_start}}}}this is a random block of text {{{{italic_end}}}}{1}"\
            .format(
                LEXICON["paragraph_start"].decode('utf-8'),
                LEXICON["paragraph_end"].decode('utf-8')
            )
    ),
    (
        b"\n{{header1_start}}this is a random block of text {{header1_end}}\n",
        "{{{{header1_start}}}}this is a random block of text {{{{header1_end}}}}"\
            .format(
                LEXICON["paragraph_start"].decode('utf-8'),
                LEXICON["paragraph_end"].decode('utf-8')
            )
    ),
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_paragraphs(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_paragraphs(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected