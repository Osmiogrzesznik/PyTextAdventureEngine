
# DICT Or That


def anyWords(L1, L2):
    return len(list(set(L1).intersection(set(L2))))


def byKey(dictionary, dct_key, default):
    """Dict Or That - Returns either dictionary value for dict_key or default"""
    r = dictionary[dct_key] if dct_key in dictionary else default
    return r


def byKeyOrSubAlt(dictionary, searched_name, default, retkey=False):
    """Returns either dictionary value for dict_key, dictionary value if one of items meets alt name or default"""
    ret = byKey(dictionary, searched_name, False)  # try directly keyed first
    if not ret:
        # loop through all dictionary entries
        for obkey in dictionary:
            ob = dictionary[obkey]
            # check if searched name matches alternative names stored in entry data ('alt')
            if 'alt' in ob and searched_name in ob['alt']:
                ret = ob
                key = obkey
                break  # return matched object and stop loop
        # all objects/entries searched and no alt was found
        if ret:
            return {'key': key, 'ob': ret} if retkey else ret
            # TODO if two items are named the same should it return array
    else:
        return {'key': searched_name, 'ob': ret} if retkey else ret
