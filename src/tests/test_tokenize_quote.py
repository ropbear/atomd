from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [
    (
        b"> single line quote",
        "{0}single line quote{1}"\
            .format(
                LEXICON["quote_start"].decode('utf-8'),
                LEXICON["quote_end"].decode('utf-8')
            )
    ),
    (
        b"> single line quote\n> multi-line quote",
        "{0}single line quote\nmulti-line quote{1}"\
            .format(
                LEXICON["quote_start"].decode('utf-8'),
                LEXICON["quote_end"].decode('utf-8')
            )
    ),
    (
        b"> single line quote\n> multi-line quote\n",
        "{0}single line quote\nmulti-line quote\n{1}"\
            .format(
                LEXICON["quote_start"].decode('utf-8'),
                LEXICON["quote_end"].decode('utf-8')
            )
    ),
    (
        b"> single line quote\n>> nested multi-line quote\n> more lines\n",
        "{0}single line quote\n{0}nested multi-line quote\n{1}more lines\n{1}"\
            .format(
                LEXICON["quote_start"].decode('utf-8'),
                LEXICON["quote_end"].decode('utf-8')
            )
    ),
    (
        b">not a quote",
        b">not a quote"
    ),
    (
        b"> single line quote\n>>not nested multi-line quote\n> more lines\n",
        "{0}single line quote\n{1}>>not nested multi-line quote\n{0}more lines\n{1}"\
            .format(
                LEXICON["quote_start"].decode('utf-8'),
                LEXICON["quote_end"].decode('utf-8')
            )
    ),
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_quote(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_quote(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected