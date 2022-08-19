from exceptions import NotBoolConvertedType, NotIntType


def build_query(it, cmd, value):
    res = list(map(lambda v: v.strip(), it))
    if cmd == 'filter':
        res = filter(lambda v: value in v, res)
    if cmd == 'sort':
        if value == "True":
            value = True
        elif value == "False":
            value = False
        else:
            raise NotBoolConvertedType
        res = sorted(res, reverse=value)
        print(list(res))
    if cmd == 'unique':
        res = set(res)
    try:
        if cmd == 'limit':
            res = list(res[:int(value)])
        if cmd == 'map':
            res = map(lambda v: v.split(' ')[int(value)], res)
    except ValueError:
        raise NotIntType
    return res
