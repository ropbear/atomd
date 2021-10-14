from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [
    (
        b"# header1",
        "{0}header1{1}".format(
            LEXICON["header1_start"].decode('utf-8'),
            LEXICON["header1_end"].decode('utf-8')
        )
    ),
    (
        b"## header2",
        "{0}header2{1}".format(
            LEXICON["header2_start"].decode('utf-8'),
            LEXICON["header2_end"].decode('utf-8')
        )
    ),
    (
        b"### header3",
        "{0}header3{1}".format(
            LEXICON["header3_start"].decode('utf-8'),
            LEXICON["header3_end"].decode('utf-8')
        )
    ),
    (
        b"#### header4",
        "{0}header4{1}".format(
            LEXICON["header4_start"].decode('utf-8'),
            LEXICON["header4_end"].decode('utf-8')
        )
    ),
    (
        b"##### header5",
        "{0}header5{1}".format(
            LEXICON["header5_start"].decode('utf-8'),
            LEXICON["header5_end"].decode('utf-8')
        )
    ),
    (
        b"###### header6",
        "{0}header6{1}".format(
            LEXICON["header6_start"].decode('utf-8'),
            LEXICON["header6_end"].decode('utf-8')
        )
    ),
    (
        b"#header1",
        "#header1"
    ),
    (
        b"##header2",
        "##header2"
    ),
    (
        b"###header3",
        "###header3"
    ),
    (
        b"####header4",
        "####header4"
    ),
    (
        b"#####header5",
        "#####header5"
    ),
    (
        b"######header6",
        "######header6"
    ),
    (
        b"#\nheader1",
        "#\nheader1"
    ),
    (
        b"##\nheader2",
        "##\nheader2"
    ),
    (
        b"###\nheader3",
        "###\nheader3"
    ),
    (
        b"####\nheader4",
        "####\nheader4"
    ),
    (
        b"#####\nheader5",
        "#####\nheader5"
    ),
    (
        b"######\nheader6",
        "######\nheader6"
    ),
    (
        b"# \nheader1",
        "# \nheader1"
    ),
    (
        b"## \nheader2",
        "## \nheader2"
    ),
    (
        b"### \nheader3",
        "### \nheader3"
    ),
    (
        b"#### \nheader4",
        "#### \nheader4"
    ),
    (
        b"##### \nheader5",
        "##### \nheader5"
    ),
    (
        b"###### \nheader6",
        "###### \nheader6"
    ),
    (
        b"# a\nheader1",
        "{0}a{1}\nheader1".format(
            LEXICON["header1_start"].decode('utf-8'),
            LEXICON["header1_end"].decode('utf-8')
        )
    ),
    (
        b"## a\nheader2",
        "{0}a{1}\nheader2".format(
            LEXICON["header2_start"].decode('utf-8'),
            LEXICON["header2_end"].decode('utf-8')
        )
    ),
    (
        b"### a\nheader3",
        "{0}a{1}\nheader3".format(
            LEXICON["header3_start"].decode('utf-8'),
            LEXICON["header3_end"].decode('utf-8')
        )
    ),
    (
        b"#### a\nheader4",
        "{0}a{1}\nheader4".format(
            LEXICON["header4_start"].decode('utf-8'),
            LEXICON["header4_end"].decode('utf-8')
        )
    ),
    (
        b"##### a\nheader5",
        "{0}a{1}\nheader5".format(
            LEXICON["header5_start"].decode('utf-8'),
            LEXICON["header5_end"].decode('utf-8')
        )
    ),
    (
        b"###### a\nheader6",
        "{0}a{1}\nheader6".format(
            LEXICON["header6_start"].decode('utf-8'),
            LEXICON["header6_end"].decode('utf-8')
        )
    ),
]

for i in range(len(test_cases)):
    test_cases[i] = (
        tokenize_headers(test_cases[i][0]),
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_tokenize_headers(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected