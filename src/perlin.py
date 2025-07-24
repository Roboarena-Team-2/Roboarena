import random
from math import floor


def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(a, b, t):
    return a + t * (b - a)


def grad(hash, x, y):
    h = hash & 3
    u = x if h < 2 else y
    v = y if h < 2 else x
    return (u if h & 1 == 0 else -u) + (v if h & 2 == 0 else -v)


class Perlin:
    def __init__(self, seed=None):
        self.p = list(range(256))
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.p)
        self.p += self.p

    def noise(self, x, y):
        xi = floor(x) & 255
        yi = floor(y) & 255
        xf = x - floor(x)
        yf = y - floor(y)

        u = fade(xf)
        v = fade(yf)

        aa = self.p[self.p[xi] + yi]
        ab = self.p[self.p[xi] + yi + 1]
        ba = self.p[self.p[xi + 1] + yi]
        bb = self.p[self.p[xi + 1] + yi + 1]

        x1 = lerp(grad(aa, xf, yf), grad(ba, xf - 1, yf), u)
        x2 = lerp(grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1), u)

        return lerp(x1, x2, v)
