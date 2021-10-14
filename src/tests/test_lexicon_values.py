from ..atomd.lexer import *
from .helpers import *
import pytest

lexicon = [(key,LEXICON[key]) for key in LEXICON.keys()]

@pytest.mark.parametrize("key, value", lexicon)
def test_lexicon_values(key,value):
    assert is_empty_or_none(key) == False
    assert is_empty_or_none(value) == False
