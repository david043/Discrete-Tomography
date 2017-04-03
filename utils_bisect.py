#!/usr/bin/env python3
from bisect import bisect_right, bisect_left


def find_gt(lst, item):  # find leftmost value greater than item
    i = bisect_right(lst, item)
    return i, lst[i]


def find_lt(lst, item):  # find rightmost value less than item
    i = bisect_left(lst, item)
    return i - 1, lst[i - 1]


def find_eq(lst, item):  # find item in list or return an error
    i = bisect_left(lst, item)
    assert item == lst[i]
    return i, lst[i]
