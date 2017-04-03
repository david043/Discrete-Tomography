#!/usr/bin/env python3
import numpy as np


def pixs_to_dt(pixs):
    rows = np.sum(pixs, axis=1)
    cols = np.sum(pixs, axis=0)
    return pixs, rows, cols

def gen_random_pixs(n_rows, n_cols, p=.5):
    return np.random.choice([0, 1], size=(n_rows, n_cols), p=[1 - p, p])

def gen_specific_dt(n_rows, n_cols, nb=0):
    binb = np.binary_repr(nb, width=n_rows * n_cols)
    binb = " ".join(c for c in binb)
    pixs = np.fromstring(binb, dtype=int, sep=" ")
    return np.resize(pixs, new_shape=(n_rows, n_cols))


if __name__ == '__main__':
    pixs, rows, cols = pixs_to_dt(gen_random_pixs(4, 3, .5))
    print(pixs)
    print(rows)
    print(cols)
    print()

    pixs, rows, cols = pixs_to_dt(gen_specific_dt(4, 3, 45312))
    print(pixs)
    print(rows)
    print(cols)
