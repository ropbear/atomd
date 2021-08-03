# atomd

A markdown lexer and parser which gives the programmer atomic control over markdown parsing to html.

Atomd tokenizes first with the lexer, so parsers for other formats can be built faster and with less code.

## Lexer

This functionality tokenizes the markdown based on the lexicon, which is a mapping of markdown syntax to tokens that will represent the specific syntax. Tokenization is done with a series of regular expressions.

## Parsers

Currently, `html.py` is the only provided parser. The `parser()` function takes tokenized markdown and replaces tokens and returns the proper html.

## Usage

A function in `atomd.py` called `md2html()` is provided to wrap both of these features together, allowing for easy use.

If you want to parse a markdown file, do the following:

```python
from atomd import md2html

html = md2html(filename="path/to/myfile.md").decode('utf-8')
```

If you want to parse a string of markdown, do the following:

```python
from atomd import md2html

html = md2html(md=b"# My markdown ByteString!").decode('utf-8')
```
