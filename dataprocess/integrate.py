import numpy as np


def trapezoid(y, x):
    a, b = x[0], x[-1]
    N = len(x)
    y_right = y[1:]
    y_left = y[:-1]
    dx = (b - a) / N
    T = dx / 2 * sum(y_right + y_left)
    return T


def simpson(y, x):
    a, b = x[0], x[-1]
    N = len(x)
    y4 = y[1:-1:2]
    y2 = y[2:-2:2]

    dx = (b - a) / N
    T = dx / 3 * (sum(y2) * 2 + sum(y4) * 4 + y[0] + y[-1])
    return T


def simpson3_8(y, x):
    a, b = x[0], x[-1]
    N = len(x)

    y0 = y[0:-1:3]
    y3 = y[3::3]
    y1 = y[1:-1:3]
    y2 = y[2:-1:3]

    dx = (b - a) / N
    T = dx * 3 / 8 * (sum(y0) + sum(y1) * 3 + sum(y2) * 3 + sum(y3))
    return T


def integrate_cumulative(y, x, name='trapezoid'):
    if name == 'simpson':
        f = simpson
    elif name == 'simpson3/8':
        f = simpson3_8
    else:
        f = trapezoid
    integrals = []
    for i in range(len(y)):
        integrals.append(f(y[:i + 1], x[:i + 1]))
    return np.abs(integrals)
