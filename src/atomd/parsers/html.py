import re
from ..lexer import LEXICON

MAP = {
    "space":                b" ",
    "horizontal_tab":       b"    ",
    "newline":              b"",
    "codeblock_start":      b"<pre><code>",
    "codeblock_end":        b"</code></pre>",
    "header1_start":        b"<h1>",
    "header1_end":          b"</h1>",
    "header2_start":        b"<h2>",
    "header2_end":          b"</h2>",
    "header3_start":        b"<h3>",
    "header3_end":          b"</h3>",
    "header4_start":        b"<h4>",
    "header4_end":          b"</h4>",
    "header5_start":        b"<h5>",
    "header5_end":          b"</h5>",
    "header6_start":        b"<h6>",
    "header6_end":          b"</h6>",
    "bold_start":           b"<strong>",
    "bold_end":             b"</strong>",
    "italic_start":         b"<em>",
    "italic_end":           b"</em>",
    "quote_start":          b"<blockquote>",
    "quote_end":            b"</blockquote>",
    "ordered_list_start":   b"<ol>",
    "ordered_list_end":     b"</ol>",
    "unordered_list_start": b"<ul>",
    "unordered_list_end":   b"</ul>",
    "list_item_start":      b"<li>",
    "list_item_end":        b"</li>",
    "inline_code_start":    b"<code>",
    "inline_code_end":      b"</code>",
    "image_link_start":     b"<img alt='",
    "image_link_middle":    b"' src='",
    "image_link_end":       b"'>",
    "escaped_pound":        b"#",
    "escaped_backtick":     b"`",
    "paragraph_start":      b"<p>",
    "paragraph_end":        b"</p>"
}

def parse_hyperlinks(html):
    """Special parsing function for hyperlinks."""
    text_tokens = re.search(LEXICON["link_start"]+b".*?"+LEXICON["link_middle"],html)
    if text_tokens is None:
        return html
    else:
        text_tokens = text_tokens.group()
        href_tokens = re.search(LEXICON["link_middle"]+b".*?"+LEXICON["link_end"],html)
        href_tokens = href_tokens.group()
        text = text_tokens.replace(LEXICON["link_start"],b"")
        text = text.replace(LEXICON["link_middle"],b"")
        href = href_tokens.replace(LEXICON["link_middle"],b"")
        href = href.replace(LEXICON["link_end"],b"")
        link = b"<a href='"+href+b"'>"+text+b"</a>"
        new_html = re.sub(
                    LEXICON["link_start"]+b".*?"+LEXICON["link_end"],
                    link,
                    html,
                    count = 1
                )
        return parse_hyperlinks(new_html)

def parser(tokenized_md):
    if tokenized_md is None:
        return None
    html = tokenized_md
    for key in MAP.keys():
        html = html.replace(LEXICON[key],MAP[key])
    html = parse_hyperlinks(html)
    return html