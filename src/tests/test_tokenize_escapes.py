from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [ #(original,expected)
    (b"\#",LEXICON["escaped_pound"]),
    (b"\`",LEXICON["escaped_backtick"]),
    (
        b"\# escaped pound single line",
        "{0} escaped pound single line"\
            .format(
                LEXICON["escaped_pound"].decode('utf-8')
            )
    ),
    (
        b"\` escaped backtick single line",
        "{0} escaped backtick single line"\
            .format(
                LEXICON["escaped_backtick"].decode('utf-8')
            )
    ),
    (
        b"\# Not a title\n\` not inline code \`",
        "{0} Not a title\n{1} not inline code {1}"\
            .format(
                LEXICON["escaped_pound"].decode('utf-8'),
                LEXICON["escaped_backtick"].decode('utf-8')
            )
    ),
    (
        b"escaped pound \# middle line",
        "escaped pound {0} middle line"\
            .format(
                LEXICON["escaped_pound"].decode('utf-8')
            )
    ),
    (
        b"escaped backtick \` middle line",
        "escaped backtick {0} middle line"\
            .format(
                LEXICON["escaped_backtick"].decode('utf-8')
            )
    ),
    (
        b"\# Not \# a title\n\` not \` inline code \`",
        "{0} Not {0} a title\n{1} not {1} inline code {1}"\
            .format(
                LEXICON["escaped_pound"].decode('utf-8'),
                LEXICON["escaped_backtick"].decode('utf-8')
            )
    ),
    (
        b"\#\`",
        "{0}{1}"\
            .format(
                LEXICON["escaped_pound"].decode('utf-8'),
                LEXICON["escaped_backtick"].decode('utf-8')
            )
    ),
    (
        b"\`\#",
        "{1}{0}"\
            .format(
                LEXICON["escaped_pound"].decode('utf-8'),
                LEXICON["escaped_backtick"].decode('utf-8')
            )
    ),
    (
        b"\#\#",
        "{0}{0}"\
            .format(
                LEXICON["escaped_pound"].decode('utf-8')
            )
    ),
    (
        b"\`\`",
        "{0}{0}"\
            .format(
                LEXICON["escaped_backtick"].decode('utf-8')
            )
    ),
    (
        b"\\\`",
        "\{0}"\
            .format(
                LEXICON["escaped_backtick"].decode('utf-8')
            )
    ),
        (
        b"\\\#",
        "\{0}"\
            .format(
                LEXICON["escaped_pound"].decode('utf-8')
            )
    ),
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_escapes(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_escapes(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected
    
