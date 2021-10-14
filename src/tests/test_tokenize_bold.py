from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [
    (
        b"****",
        "{0}{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"**bold**",
        "{0}bold{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"**",
        b"**"
    ),
    (
        b"**bold*asterisk**",
        "{0}bold*asterisk{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"*****",
        "{0}*{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"***asdf***",
        "{0}*asdf*{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"******",
        "{0}**{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"****",
        "{0}{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"**bold**",
        "{0}bold{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"__bold**",
        "{0}bold{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"**bold__",
        "{0}bold{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"__",
        b"__"
    ),
    (
        b"__bold_asterisk__",
        "{0}bold_asterisk{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"_____",
        "{0}_{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"___asdf___",
        "{0}_asdf_{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"______",
        "{0}__{1}".format(
            LEXICON["bold_start"].decode('utf-8'),
            LEXICON["bold_end"].decode('utf-8')
        )
    ),
    (
        b"_*bold_asterisk*_",
        "_*bold_asterisk*_"
    ),
    (
        b"_*_*_",
        "_*_*_"
    ),
    (
        b"_*_asdf_*_",
        "_*_asdf_*_"
    ),
    (
        b"_*__*_",
        "_*__*_"
    ),
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_bold(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_bold(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected