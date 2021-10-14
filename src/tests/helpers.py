def is_empty(string):
    if string == '' or string == b'':
        return True
    else:
        return False

def is_empty_or_none(string):
    if is_empty(string) or string is None:
        return True
    else:
        return False