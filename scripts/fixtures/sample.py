def add(a, b):
    # BUG: should add, actually subtracts
    return a - b


def total(xs):
    s = 0
    for x in xs:
        s = add(s, x)
    return s
