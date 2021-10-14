from ..atomd.lexer import *
from .helpers import *
import pytest

test_cases = [(True,True),(False,False)]

for i in range(len(test_cases)):
    test_cases[i] = (
        test_cases[i][0],
        test_cases[i][1]
    )

@pytest.mark.parametrize("tokenized, expected", test_cases)
def test_(tokenized, expected):
    if type(expected) == type(""):
        expected = bytes(expected,'utf-8')
    assert tokenized == expected