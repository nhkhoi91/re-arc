from dsl import *

def verify_cardinality_1(I: Grid) -> Grid:
    x1 = {color: colorcount(I, color) for color in palette(I)}
    x2 = argmax(x1.keys(), lambda x: x1[x])
    x3 = canvas(x2, (ONE, ONE))
    return x3


def verify_cardinality_2(I: Grid) -> Grid:
    x1 = {color: colorcount(I, color) for color in palette(I)}
    x2 = argmin(x1.keys(), lambda x: x1[x])
    x3 = canvas(x2, (ONE, ONE))
    return x3
    
def verify_cardinality_3(I: Grid) -> Grid:
    x0 = lbind(colorcount, I)
    x1 = palette(I)
    x2 = order(x1, x0)
    x3 = canvas(first(x2), (ONE, len(x1)))
    fill_operations = frozenset(
    frozenset(
        [(x2[i], (0, i))]
        ) for i in range(len(x1))
    )

    for x, op in zip(x2, fill_operations):
        x3 = fill(x3, x, op)
    return x3


def verify_cardinality_4(I: Grid) -> Grid:
    x0 = palette(I)
    x1 = mostcolor(I)
    x2 = remove(x1, x0)
    x3 = lbind(colorcount, I)
    x4 = apply(x3, x2)
    x5 = sum(x4)
    return x5