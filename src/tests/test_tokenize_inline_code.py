from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [
    (
        b"` `",
        "{0} {1}".format(
            LEXICON["inline_code_start"].decode('utf-8'),
            LEXICON["inline_code_end"].decode('utf-8')
        )
    ),
    (
        b"``",
        b"``"
    ),
    (
        b"```",
        "{0}`{1}".format(
            LEXICON["inline_code_start"].decode('utf-8'),
            LEXICON["inline_code_end"].decode('utf-8')
        )
    ),
    (
        b"`:!@#$%*()^&`",
        "{0}:!@#$%*()^&{1}".format(
            LEXICON["inline_code_start"].decode('utf-8'),
            LEXICON["inline_code_end"].decode('utf-8')
        )
    ),
    (
        b"`some_normal_code`",
        "{0}some_normal_code{1}".format(
            LEXICON["inline_code_start"].decode('utf-8'),
            LEXICON["inline_code_end"].decode('utf-8')
        )
    ),
    (
        b"`\n`",
        b"`\n`"
    ),
    (
        b"`\t`",
        "{0}\t{1}".format(
            LEXICON["inline_code_start"].decode('utf-8'),
            LEXICON["inline_code_end"].decode('utf-8')
        )
    ),
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_inline_code(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_inline_code(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected