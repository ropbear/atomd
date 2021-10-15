from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [
    (
        b"```\n\n```",
        "{0}{1}".format(
            LEXICON["codeblock_start"].decode('utf-8'),
            LEXICON["codeblock_end"].decode('utf-8')
        )
    ),
    (
        b"``````",
        b"``````"
    ),
    (
        b"\n```\n\n```\n",
        "\n{0}{1}\n".format(
            LEXICON["codeblock_start"].decode('utf-8'),
            LEXICON["codeblock_end"].decode('utf-8')
        )
    ),
    (
        b"```\nsome code\n\tsome more code\n```",
        "{0}some code\n\tsome more code{1}".format(
            LEXICON["codeblock_start"].decode('utf-8'),
            LEXICON["codeblock_end"].decode('utf-8')
        )
    ),
    (
        b"```\nsome code\n\ts```ome more code\n```",
        "{0}some code\n\ts```ome more code{1}".format(
            LEXICON["codeblock_start"].decode('utf-8'),
            LEXICON["codeblock_end"].decode('utf-8')
        )
    ),
    (
        b"```\nsome code\n\ts```om`e` more code\n```",
        "{0}some code\n\ts```om`e` more code{1}".format(
            LEXICON["codeblock_start"].decode('utf-8'),
            LEXICON["codeblock_end"].decode('utf-8')
        )
    ),
    (
        b"```\nsome code\n\ts```om`e` more code\n```",
        "{0}some code\n\ts```om`e` more code{1}".format(
            LEXICON["codeblock_start"].decode('utf-8'),
            LEXICON["codeblock_end"].decode('utf-8')
        )
    ),
    (
        b"```\ntest123\nsome code\n\ts```om`e` more code\n```",
        "{0}test123\nsome code\n\ts```om`e` more code{1}".format(
            LEXICON["codeblock_start"].decode('utf-8'),
            LEXICON["codeblock_end"].decode('utf-8')
        )
    ),
    (
        b"asdfqwer```test123\nsome code\n\ts```om`e` more code\n```asdfqwer",
        b"asdfqwer```test123\nsome code\n\ts```om`e` more code\n```asdfqwer"
    ),
    (
        b"asdfqwer```\ntest123\nsome code\n\ts```om`e` more code\n```asdfqwer",
        "asdfqwer```\ntest123\nsome code\n\ts```om`e` more code\n```asdfqwer".format(
            LEXICON["codeblock_start"].decode('utf-8')
        )
    ),
    (
        b"asdf\n```\ntest123\nsome code\n\ts```om`e` more code\n```\nasdf",
        "asdf\n{0}test123\nsome code\n\ts```om`e` more code{1}\nasdf".format(
            LEXICON["codeblock_start"].decode('utf-8'),
            LEXICON["codeblock_end"].decode('utf-8')
        )
    ),
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_codeblock(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_codeblock(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected