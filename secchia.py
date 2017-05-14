
def separatedStringToList(my_string, s=','):
    '''
    This function accept a "s" separated string and transform it in a list
    remove also all spaces.
    s is by default a comma
    '''
    my_list = my_string.split(s)
    _list = [x.strip(' ') for x in my_list]
    return _list
