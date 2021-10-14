import re
from binascii import hexlify

LEXICON = {
    "space":                b"{{space}}",
    "horizontal_tab":       b"{{horizontal_tab}}",
    "newline":              b"{{newline}}",
    "codeblock_start":      b"{{codeblock_start}}",
    "codeblock_end":        b"{{codeblock_end}}",
    "header1_start":        b"{{header1_start}}",
    "header1_end":          b"{{header1_end}}",
    "header2_start":        b"{{header2_start}}",
    "header2_end":          b"{{header2_end}}",
    "header3_start":        b"{{header3_start}}",
    "header3_end":          b"{{header3_end}}",
    "header4_start":        b"{{header4_start}}",
    "header4_end":          b"{{header4_end}}",
    "header5_start":        b"{{header5_start}}",
    "header5_end":          b"{{header5_end}}",
    "header6_start":        b"{{header6_start}}",
    "header6_end":          b"{{header6_end}}",
    "bold_start":           b"{{bold_start}}",
    "bold_end":             b"{{bold_end}}",
    "italic_start":         b"{{italic_start}}",
    "italic_end":           b"{{italic_end}}",
    "quote_start":          b"{{quote_start}}",
    "quote_end":            b"{{quote_end}}",
    "ordered_list_start":   b"{{ordered_list_start}}",
    "ordered_list_end":     b"{{ordered_list_end}}",
    "unordered_list_start": b"{{unordered_list_start}}",
    "unordered_list_end":   b"{{unordered_list_end}}",
    "list_item_start":      b"{{list_item_start}}",
    "list_item_end":        b"{{list_item_end}}",
    "inline_code_start":    b"{{inline_code_start}}",
    "inline_code_end":      b"{{inline_code_end}}",
    "image_link_start":     b"{{image_link_start}}",
    "image_link_middle":    b"{{image_link_middle}}",
    "image_link_end":       b"{{image_link_end}}",
    "link_start":           b"{{link_start}}",
    "link_middle":          b"{{link_middle}}",
    "link_end":             b"{{link_end}}",
    "escaped_pound":        b"{{escaped_pound}}",
    "escaped_backtick":     b"{{escaped_backtick}}",
    "paragraph_start":      b"{{paragraph_start}}",
    "paragraph_end":        b"{{paragraph_end}}",
    "reserved":             b"reserved"
}

class TokenExistsError(Exception):
    """
    An error raised if a token in use already exists 
    in the input about to be put through the lexer.
    """    
    def __init__(self, *args):
        if args:
            self.message = "Token already exists in file: " + hexlify(args[0]).decode('utf-8')
        else:
            self.message = None
    
    def __str__(self):
        if self.message:
            return "TokenExistsError: " + self.message
        else:
            return "TokenExistsError"

# helper functions, except recursive_list_helper

def next_match(regex,text):
    """
    @brief Check if $regex is in $text and return first occurance, else return None

    @param `regex[RawString|ByteObject]`: The regex to match against

    @param `text[ByteString]`: The bytes object to search for a match
    
    @return ByteObject | None
    """
    if type(regex) is not type(b""):
        regex = bytes(regex,'utf-8')
    match = re.search(regex,text,re.MULTILINE)
    return match if match is None else match.group()

def count_pounds(line):
    """Count the number of # at the start of a line. Used for header identification."""
    count = 0
    for c in line:
        if c == ord("\n"):
            pass
        elif c == ord("#"):
            count += 1
        else:
            return count

def left_justify(md):
    """Remove a single tab worth of whitespace from a block of text."""
    s = md.split(b"\n")
    newlines = []
    for line in s:
        newlines += [re.sub(b"^(\t|    )",b"",line)]
    s = b"\n".join(newlines)
    return s

def get_list_type(md):
    """
    @brief  Searches a block of markdown for an unordered or ordered list,
            and then returns the respective object.
    
    @param md[BytesObject]: the block of text to search

    @return None if no list found, otherwise a Dict with the type, regex,
            and sublist regex for the type of list that was discovered first.
    """
    ulist_obj = {
            "type":"unordered_list",
            "regex":r"^((\t| )*(\-|\*|\+) .*\n?)+",
            "sublist":r"^((\t| )+(\-|\*|\+) .*\n)+"
        }
    olist_obj = {
            "type":"ordered_list",
            "regex":r"^((\t| )*([0-9]+\.) .*\n?)+",
            "sublist":r"^((\t| )+([0-9]+\.) .*\n)+"
        }
    olist = next_match(olist_obj["regex"],md)
    oi = md.index(olist) if olist else None
    ulist = next_match(ulist_obj["regex"],md)
    ui = md.index(ulist) if ulist else None

    if ui is None and oi is None:
        return None
    elif oi is not None and ui is None:
        return olist_obj
    elif ui is not None and oi is None:
        return ulist_obj
    elif oi < ui:
        return olist_obj
    elif ui < oi:
        return ulist_obj
    else:
        return None

def handle_identical_list(md_list,sublist):
    """
        Handler for edge case of multiple of the same type of list
        in the same markdown. If the same list occurs more than
        once, re-join the latter sections and return them all as the
        "after" section.
    """
    if len(md_list) > 2:
        return [md_list[0], sublist.join(md_list[1:])]
    else:
        return md_list

def is_para(md):
    """Returns True if its a markdown paragraph, else false."""
    starts_with_token = False
    for key in LEXICON.keys():
        match = re.search(b"^"+LEXICON[key]+b".*",md)
        if match is not None:
            if "italic" not in key and "bold" not in key:
                starts_with_token = True
                break 
    return not starts_with_token

# tokenization functions

def tokenizer(r_match, r_start, lexicon_start, r_end, lexicon_end, md):
    """
    @brief Wrapper to avoid code duplication.
    
    @param `r_match[RawString]`:
            Regular expression that matches the entire string to be tokenized.

    @param `r_start[RawString]`:
            Regular expression to match the beginning of the desired string.

    @param `lexicon_start[ByteString]`:
            Token to place at the beginning of the match.

    @param `r_end[RawString]`:
            Regular expression matching the end of the desired string.

    @param `lexicon_end[ByteString]`:
            Token to place at the end of the match.

    @param `md[ByteString]`:
            Markdown stream.

    @return `md[ByteObject]`
    """
    # the RawString objects are converted to bytes in order to satisfy re.sub
    next = next_match(r_match,md)
    if next is None:
        return md
    start = re.sub(
            bytes(r_start,'utf-8'),
            lexicon_start,
            next,
            count=1
        )
    end = re.sub(
            bytes(r_end,'utf-8'),
            lexicon_end,
            start,
            count=1,
        )
    tokenized = md.replace(next,end)
    return tokenizer(
            r_match,
            r_start,
            lexicon_start,
            r_end,
            lexicon_end,
            tokenized
        )

def tokenize_whitespace(md):
    """Replace space, tab, and newlines."""
    tmp = md.replace(b"\t",LEXICON["horizontal_tab"])
    tmp = tmp.replace(b"\n",LEXICON["newline"])
    return tmp.replace(b" ",LEXICON["space"])

def tokenize_escapes(md):
    """Search for escape sequences and tokenize them."""
    tmp = re.sub(bytes(r"\\#",'utf-8'),LEXICON["escaped_pound"], md)
    tmp = re.sub(bytes(r"\\`",'utf-8'),LEXICON["escaped_backtick"], tmp)
    return tmp

def tokenize_codeblock(md):
    """Regex match and tokenize a markdown code block."""
    return tokenizer(
        r"^```(\n|.)+^```",
        r"(^|\n)```",
        LEXICON["codeblock_start"],
        r"(^|\n)```",
        LEXICON["codeblock_end"],
        md
    )

def tokenize_inline_code(md):
    """Regex match for inline code and tokenize it."""
    return tokenizer(
        r"`.+`",
        r"`",
        LEXICON["inline_code_start"],
        r"`(?!`)",
        LEXICON["inline_code_end"],
        md
    )

def tokenize_headers(md):
    """Regex match and tokenize headers."""
    next = next_match(r"^#{1,6} .+",md)
    if next is None:
        return md
    # get the header size/type (<h1> vs. <h4>)
    header_type = count_pounds(next)
    start = re.sub(
            bytes(r"^#{1,6} ",'utf-8'),
            LEXICON[f"header{str(header_type)}_start"],
            next,
            count=1
        )
    end = re.sub(
            b"$",
            LEXICON[f"header{str(header_type)}_end"],
            start,
            count=1
        )
    tokenized = md.replace(next,end)
    return tokenize_headers(tokenized)

def tokenize_bold(md):
    """Regex match and tokenize bolded characters."""
    return tokenizer(
        r"(\*\*|__).*(\*\*|__)",
        r"(\*\*|__)",
        LEXICON["bold_start"],
        r"(\*\*|__)(?!\*|_)",
        LEXICON["bold_end"],
        md
    )

def tokenize_italicize(md):
    """Regex match and tokenize italicized characters."""
    return tokenizer(
        r"\*.*\*",
        r"\*",
        LEXICON["italic_start"],
        r"\*(?!\*)",
        LEXICON["italic_end"],
        md
    )

def tokenize_quote(md):
    """Regex match and tokenize quoted characters."""
    next = next_match(r"^(>+ .*\n?)+",md)
    if next is None:
        return md
    lines = next.split(b"\n")
    removed = b'\n'.join([re.sub(b"(^|\n)> ?",b"",line) for line in lines])
    breakout = md.split(next)
    tokenized = breakout[0] + \
                LEXICON["quote_start"] + \
                tokenize_quote(removed) + \
                LEXICON["quote_end"] + \
                breakout[1]
    return tokenize_quote(tokenized)

def tokenize_list_item(md,nested=b""):
    """
    @brief Tokenize a single list item.
    
    @param md[ByteString]: The markdown item to parse.

    @param nested[ByteString]:  A byte string (in this case a sublist)
                                to nest in the list item.

    @return A ByteString of the tokenized list item .
    """
    if md == b"":
        return md
    start = re.sub(b"^(\-|\*|\+|[0-9]+\.) ",LEXICON["list_item_start"],md)
    return start + nested + LEXICON["list_item_end"]

def tokenize_list_items(md):
    """Tokenize list items in the passed ByteString."""
    lines = md.split(b"\n")
    newlines = []
    for line in lines:
        if line != b"":
            start = re.sub(b"^(\-|\*|\+|[0-9]+\.) ",LEXICON["list_item_start"],line)
            if LEXICON["list_item_start"] in start:
                end = re.sub(b"$",LEXICON["list_item_end"],start)
                newlines += [end]
            else:
                newlines += [line]
    return b"\n".join(newlines)

def recursive_list_helper(md,is_breakout=False):
    """Recursive helper function for tokenize_lists()"""
    list_obj = get_list_type(md)
    if list_obj is None:
        return md
    next_sublist = next_match(r"^((\t| )+(\-|\*|\+|[0-9]+\.) .*\n)+",md)
    if next_sublist is None:
        tokenized = tokenize_list_items(md)
        if is_breakout:
            return tokenized
        return LEXICON[list_obj["type"]+'_start']+tokenized+LEXICON[list_obj["type"]+'_end']
    else:
        # make the identified sublist the root list for easier parsing
        justified = left_justify(next_sublist)
        tokenized_sublist = recursive_list_helper(justified)

        # break the markdown into sections:
        #   - before the sublist
        #   - the sublist
        #   - after the sublist
        breakout = md.split(next_sublist)
        breakout = handle_identical_list(breakout,next_sublist)
        top = breakout[0].split(b"\n")
        # remove empty lines, which can occur if one newline follows another
        while b"" in top: top.remove(b"")

        # both of these next calls specify they are a breakout, which stops from 
        # tokenizing each section of the root list which are divided by sublists

        # recursive call on the top section, except the line right above the sublist
        # since we need to nest the sublist into that list item
        tokenized_top = recursive_list_helper(b"\n".join(top[:-1]),is_breakout=True)
        # recursive call on the bottom section
        tokenized_bottom = recursive_list_helper(breakout[1],is_breakout=True)


        # tokenize the line right above the sublist, and nest the sublist within the list item
        # note that this function call is separate from tokenize_list_items()
        parent_and_sublist = tokenize_list_item(top[-1],nested=tokenized_sublist)
        # if we're in a breakout recursive call of a root list, do not tokenize
        if is_breakout:
            return tokenized_top + parent_and_sublist + tokenized_bottom
        # otherwise we're in the root list and should wrap everything in a token pair
        return LEXICON[list_obj["type"]+'_start'] + \
            tokenized_top + parent_and_sublist + tokenized_bottom + \
            LEXICON[list_obj["type"]+'_end']

def tokenize_lists(md):
    """Regex match and tokenize lists and their list items"""
    next_list = next_match(r"^((\t| )*(\-|\*|\+|[0-9]+\.) .*\n)+",md)
    if next_list is None:
        return md
    tokenized = recursive_list_helper(next_list).replace(b"\n",b"")
    replaced = md.replace(next_list,tokenized)
    return tokenize_lists(replaced)

def tokenize_image_link(md):
    """Regex match and tokenize an image link"""
    next = next_match(r"\!\[.*\]\(.*\)",md)
    if next is None:
        return md
    start = re.sub(
            bytes(r"\!\[",'utf-8'),
            LEXICON["image_link_start"],
            next,
            count=1
        )
    mid = re.sub(
            bytes(r"\]\(",'utf-8'),
            LEXICON["image_link_middle"],
            start,
            count=1
        )
    end = re.sub(
            bytes(r"\)",'utf-8'),
            LEXICON["image_link_end"],
            mid,
            count=1
        )
    tokenized = md.replace(next,end)
    return tokenize_image_link(tokenized)
    
def tokenize_hyperlink(md):
    """Regex match and tokenize a hyperlink"""
    next = next_match(r"\[.*\]\(.*\)",md)
    if next is None:
        return md
    start = re.sub(
            bytes(r"\[",'utf-8'),
            LEXICON["link_start"],
            next,
            count=1
        )
    mid = re.sub(
            bytes(r"\]\(",'utf-8'),
            LEXICON["link_middle"],
            start,
            count=1
        )
    end = re.sub(
            bytes(r"\)",'utf-8'),
            LEXICON["link_end"],
            mid,
            count=1
        )
    tokenized = md.replace(next,end)
    return tokenize_hyperlink(tokenized)

def tokenize_paragraphs(md):
    """Tokenize the un-tokenized content as paragraphs."""
    lines = md.split(b"\n")
    newlines = []
    for line in lines:
        if line == b"":
            pass
        elif is_para(line):
            newlines += [
                LEXICON["paragraph_start"] + \
                line + \
                LEXICON["paragraph_end"]
            ]
        else:
            newlines += [line]
    return b"\n".join(newlines)

def validate_input(md):
    """Checks markdown byte stream to see if any tokens already exist."""
    for key in LEXICON.keys():
        if LEXICON[key] in md:
            raise TokenExistsError(LEXICON[key])

def lexer(filename=None,md=None):
    """
    @brief  Takes the markdown and tokenizes based on the pre-defined grammar for
            easier use by the parser.

    @param `filename[str]`: The filename to parse.

    @return A tokenized template on success, None on failure.
    """
    if md is None:
        try:
            f = open(filename,"rb")
            md = f.read()
        except (OSError, IOError) as e:
            # OSError captures both PermissionError and FileNotFoundError
            print("[!] Markdown file open error: %s " % e)
            return None

    #check that none of the tokens already exist in the file
    try:
        validate_input(md)
    except TokenExistsError as e:
        print("[!] " + str(e))
        return None

    # each tkn_* variable denotes the markdown after being tokenized
    # for whichever character is after the tkn_ prefix.
    # This allows for order of precedence in encoding, making it easier
    # to write things such as "nothing in a code block should be parsed".
    tkn_escape = tokenize_escapes(md)
    tkn_codeblocks = tokenize_codeblock(tkn_escape)
    tkn_inline_code = tokenize_inline_code(tkn_codeblocks)
    tkn_headers = tokenize_headers(tkn_inline_code)
    tkn_bold = tokenize_bold(tkn_headers)
    tkn_italic = tokenize_italicize(tkn_bold)
    tkn_quote = tokenize_quote(tkn_italic)
    tkn_lists = tokenize_lists(tkn_quote)
    tkn_img_links = tokenize_image_link(tkn_lists)
    tkn_hyperlinks = tokenize_hyperlink(tkn_img_links)
    tkn_paragraphs = tokenize_paragraphs(tkn_hyperlinks)
    tkn_whitespace = tokenize_whitespace(tkn_paragraphs)
    return tkn_whitespace
