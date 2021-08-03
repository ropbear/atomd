from .lexer import lexer
from .parsers.html import parser as to_html

def md2html(filename=b"",md=None):
    """
    @brief Wrapper for lexer and parser.

    @param `filename[str]`: The filename to parse.

    @return Parsed HTML on success, None if failure occurred.
    """
    if md is not None:
        template = lexer(md=md)
    else:
        template = lexer(filename=filename)
    return to_html(template)
