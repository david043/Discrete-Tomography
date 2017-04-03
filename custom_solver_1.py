#!/usr/bin/env python3
import bisect
import sortedcontainers


class Prob:

    def __init__(self, val, crd):
        self.val = val  # product of row and column probabilities
        self.crd = crd  # coordinates in the matrix

    def __lt__(self, other):
        if type(self.val) != type(other.val):  # one is a bool, the other is a float
            return self.val is False or other.val is True  # False first, True last
        if self.val == other.val:
            if self.crd[0] == other.crd[0]:
                return self.crd[1] < other.crd[1]  # col decides
            return self.crd[0] < other.crd[0]  # row decides
        return self.val < other.val  # val decides

    def __repr__(self):
        return ("(" + str(self.crd[0]) + "," + str(self.crd[1]) + "):"  # crd
                + (str(self.val) if type(self.val) is bool else "{0:.2f}".format(self.val)))  # val


def print_mat(mat, ones_li_row, ones_li_col):
    csize, sep, sep_col = 5, "", "|"
    header = " " * csize + sep_col + sep.join(str(c).rjust(csize) for c in ones_li_col) + sep_col
    print(header)
    print("-" * len(header))
    for r in range(len(ones_li_row)):
        print(str(ones_li_row[r]).ljust(csize), end=sep_col)
        for c in range(len(mat[r])):
            if mat[r][c].val is True:
                print("█" * csize, end=sep)  # U+2588
            elif mat[r][c].val is False:
                print("░" * csize, end=sep)  # U+2591
            else:
                print("{0:.2f}".format(mat[r][c].val).rjust(csize), end=sep)
        print("\b" * len(sep) + sep_col)
    print("-" * len(header))


rows = [2, 1, 2]
cols = [1, 2, 2]
n_rows = len(rows)
n_cols = len(cols)
assert sum(rows) == sum(cols)


mat = [[Prob((rows[r] * cols[c]) / (n_rows * n_cols), (r, c))
        for c in range(n_cols)] for r in range(n_rows)]
lst = sortedcontainers.SortedList(p for row in reversed(mat) for p in reversed(row))
ones_li_row = list(rows)  # number of ones left in each row
ones_li_col = list(cols)  # number of ones left in each column
pixs_li_row = [n_cols] * n_rows  # number of pixels left unassigned in each row
pixs_li_col = [n_rows] * n_cols  # number of pixels left unassigned in each column


def assign(r, c, val):
    mat[r][c].val = val
    pixs_li_row[r] -= 1
    pixs_li_col[c] -= 1
    if val is True:
        ones_li_row[r] -= 1
        ones_li_col[c] -= 1

    assert type(val) is bool
    assert pixs_li_row[r] == len([1 for c in range(n_cols) if type(mat[r][c].val) is not bool])
    assert pixs_li_col[c] == len([1 for r in range(n_rows) if type(mat[r][c].val) is not bool])
    assert ones_li_row[r] == rows[r] - len([1 for c in range(n_cols) if mat[r][c].val is True])
    assert ones_li_col[c] == cols[c] - len([1 for r in range(n_rows) if mat[r][c].val is True])


def update(r, c):
    if mat[r][c].val is True or mat[r][c].val is False:
        pass
    elif ones_li_row[r] == 0 or ones_li_row[r] == pixs_li_row[r]:
        mat[r][c].val = 0. if ones_li_row[r] == 0 else 1.
    elif ones_li_col[c] == 0 or ones_li_col[c] == pixs_li_col[c]:
        mat[r][c].val = 0. if ones_li_col[c] == 0 else 1.
    else:
        mat[r][c].val = (ones_li_row[r] / pixs_li_row[r]) * (ones_li_col[c] / pixs_li_col[c])


def find_gt(lst, item):  # find leftmost value greater than item
    i = bisect.bisect_right(lst, item)
    return i, lst[i]


def find_lt(lst, item):  # find rightmost value less than item
    i = bisect.bisect_left(lst, item)
    return i - 1, lst[i - 1]


def find_eq(lst, item):  # find item in list or return an error
    i = bisect.bisect_left(lst, item)
    assert item == lst[i]
    return i, lst[i]


for i in range(n_rows * n_cols):  # FIXME range
    # print the matrix and the sorted list
    print_mat(mat, ones_li_row, ones_li_col)
    print(str(lst) + "\n")

    # detect the probabilities that are at the extremes
    lower_pos, lower_prob = find_gt(lst, Prob(-1., None))
    lower_dist = lower_prob.val**.5
    upper_pos, upper_prob = find_lt(lst, Prob(2., None))
    upper_dist = 1 - upper_prob.val**.5

    # decide which one to select
    pos = lower_pos if lower_dist < upper_dist else upper_pos
    prob = lower_prob if lower_dist < upper_dist else upper_prob
    assert type(prob.val) is not bool
    r, c = prob.crd

    # assign the most probable value to the pixel accordingly
    assignement = prob.val**.5 > .5
    assign(r, c, assignement)  # FIXME: add only Trues and debug the constraints there
    del lst[pos]
    lst.add(prob)

    # update the row and column of this assignement
    for row in range(n_rows):
        pos_tmp, prob_tmp = find_eq(lst, mat[row][c])
        update(row, c)
        del lst[pos_tmp]
        lst.add(prob_tmp)
    for col in range(n_cols):
        pos_tmp, prob_tmp = find_eq(lst, mat[r][col])
        update(r, col)
        del lst[pos_tmp]
        lst.add(prob_tmp)

# print the final result
print_mat(mat, ones_li_row, ones_li_col)
print(str(lst) + "\n")
