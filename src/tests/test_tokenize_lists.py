from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [
    (
        b"1. ordered list\n2.  item two\n",
        "{0}{2}ordered list{3}{2} item two{3}{1}"\
            .format(
                LEXICON["ordered_list_start"].decode('utf-8'),
                LEXICON["ordered_list_end"].decode('utf-8'),
                LEXICON["list_item_start"].decode('utf-8'),
                LEXICON["list_item_end"].decode('utf-8'),
            )
    ),
    (
        b"1. ordered list\n\t- sub-item one\n",
        "{0}{2}ordered list{4}{2}sub-item one{3}{5}{3}{1}"\
            .format(
                LEXICON["ordered_list_start"].decode('utf-8'),
                LEXICON["ordered_list_end"].decode('utf-8'),
                LEXICON["list_item_start"].decode('utf-8'),
                LEXICON["list_item_end"].decode('utf-8'),
                LEXICON["unordered_list_start"].decode('utf-8'),
                LEXICON["unordered_list_end"].decode('utf-8'),
            )
    ),
    (
        b"1. ordered list\n\t- sub-item one\n2. asdfqwer\n",
        "{0}{2}ordered list{4}{2}sub-item one{3}{5}{3}{2}asdfqwer{3}{1}"\
            .format(
                LEXICON["ordered_list_start"].decode('utf-8'),
                LEXICON["ordered_list_end"].decode('utf-8'),
                LEXICON["list_item_start"].decode('utf-8'),
                LEXICON["list_item_end"].decode('utf-8'),
                LEXICON["unordered_list_start"].decode('utf-8'),
                LEXICON["unordered_list_end"].decode('utf-8'),
            )
    ),
    (
        b"1. ordered list\n\t- sub-item one\n2. asdfqwer\n",
        "{0}{2}ordered list{4}{2}sub-item one{3}{5}{3}{2}asdfqwer{3}{1}"\
            .format(
                LEXICON["ordered_list_start"].decode('utf-8'),
                LEXICON["ordered_list_end"].decode('utf-8'),
                LEXICON["list_item_start"].decode('utf-8'),
                LEXICON["list_item_end"].decode('utf-8'),
                LEXICON["unordered_list_start"].decode('utf-8'),
                LEXICON["unordered_list_end"].decode('utf-8'),
            )
    ),
    (
        b"-a\n-b\n-c\n",
        "-a\n-b\n-c\n"
    ),
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_lists(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_lists(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected