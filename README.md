# atomd

### Version 0.2.4

A markdown lexer and parser which gives the developer atomic control over markdown parsing to html.

Atomd first tokenizes the markdown with the lexer.

Using the tokenized markdown, parsers for various different markup languages (HTML, XML, etc) are easier to implement, since it more or less becomes a game of find and replace.

## Install

```
python3 -m pip install atomd
```

## Usage

Functions in `atomd.py` called `md2<target_language>()` combine the lexer and parser to provide an easier calling convention.

In the case of the HTML parser, this is `md2html()`.

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

## Lexer

This portion of the program tokenizes the markdown based on the lexicon, which is a mapping of markdown syntax items to tokens that will represent the specific syntax.

**Tokenization is done with a series of regular expressions**.

If there are bugs in the program, it is likely they exist in the regular expressions and can be fixed without significant design changes to the program, which allows for quick turnaround on bugfixes.

## Parsers

Currently, atomd supports the following:

- HTML (`html.py`)


