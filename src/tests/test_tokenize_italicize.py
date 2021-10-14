from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [
    (
        b"**",
        "{0}{1}".format(
            LEXICON["italic_start"].decode('utf-8'),
            LEXICON["italic_end"].decode('utf-8')
        )
    ),
    (
        b"*italic*",
        "{0}italic{1}".format(
            LEXICON["italic_start"].decode('utf-8'),
            LEXICON["italic_end"].decode('utf-8')
        )
    ),
    (
        b"*",
        b"*"
    ),
    (
        b"***",
        "{0}*{1}".format(
            LEXICON["italic_start"].decode('utf-8'),
            LEXICON["italic_end"].decode('utf-8')
        )
    ),
    (
        b"***asdf***",
        "{0}{0}{1}asdf{0}{1}{1}".format(
            LEXICON["italic_start"].decode('utf-8'),
            LEXICON["italic_end"].decode('utf-8')
        )
    ),
    (
        b"******",
        "{0}{0}{0}{1}{1}{1}".format(
            LEXICON["italic_start"].decode('utf-8'),
            LEXICON["italic_end"].decode('utf-8')
        )
    ),
    # (
    #     b"_",
    #     b"_"
    # ),
    # (
    #     b"__",
    #     "{0}{1}".format(
    #         LEXICON["italic_start"].decode('utf-8'),
    #         LEXICON["italic_end"].decode('utf-8')
    #     )
    # ),
    # (
    #     b"_italic_",
    #     "{0}italic{1}".format(
    #         LEXICON["italic_start"].decode('utf-8'),
    #         LEXICON["italic_end"].decode('utf-8')
    #     )
    # ),
    # (
    #     b"___",
    #     "{0}_{1}".format(
    #         LEXICON["italic_start"].decode('utf-8'),
    #         LEXICON["italic_end"].decode('utf-8')
    #     )
    # ),
    # (
    #     b"___asdf___",
    #     "{0}__asdf__{1}".format(
    #         LEXICON["italic_start"].decode('utf-8'),
    #         LEXICON["italic_end"].decode('utf-8')
    #     )
    # ),
    # (
    #     b"______",
    #     "{0}{1}{0}{1}{0}{1}".format(
    #         LEXICON["italic_start"].decode('utf-8'),
    #         LEXICON["italic_end"].decode('utf-8')
    #     )
    # ),
    # (
    #     b"_italic*",
    #     "{0}italic{1}".format(
    #         LEXICON["italic_start"].decode('utf-8'),
    #         LEXICON["italic_end"].decode('utf-8')
    #     )
    # ),
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_italicize(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_italicize(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected