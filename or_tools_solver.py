#!/usr/bin/env python3
import argparse
from ortools.constraint_solver import pywrapcp
from timeit import default_timer as timer


def solve(row_sums, col_sums, find_all=False):
    # initialization
    solver = pywrapcp.Solver("dt")
    n_rows = len(row_sums)
    n_cols = len(col_sums)

    # declare variables
    x = []
    for i in range(n_rows):
        t = []
        for j in range(n_cols):
            t.append(solver.IntVar(0, 1, "x[%i,%i]" % (i, j)))
        x.append(t)
    x_flat = [x[i][j] for i in range(n_rows) for j in range(n_cols)]

    # constraints
    [solver.Add(solver.Sum([x[i][j] for j in range(n_cols)]) == row_sums[i]) for i in range(n_rows)]
    [solver.Add(solver.Sum([x[i][j] for i in range(n_rows)]) == col_sums[j]) for j in range(n_cols)]

    # solution and search
    solution = solver.Assignment()
    solution.Add(x_flat)

    # db: DecisionBuilder
    db = solver.Phase(x_flat, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
    solver.NewSearch(db)

    # find the solution(s)
    start = timer()
    if not find_all:  # if only one solution has to be printed
        solver.NextSolution()
        #print_solution(x, n_rows, n_cols, row_sums, col_sums)
    else:  # if all the solutions have to be printed
        num_solutions = 0
        while solver.NextSolution():
            #print_solution(x, n_rows, n_cols, row_sums, col_sums)
            #print()
            num_solutions += 1
        solver.EndSearch()
        print("num_solutions:", num_solutions)

    # print statistics about the resolution
    # print("failures:", solver.Failures())
    # print("branches:", solver.Branches())
    # print("WallTime:", solver.WallTime())
    # print("{0:.3f}".format(timer() - start), "s", sep="")


def print_solution(x, rows, cols, row_sums, col_sums):
    print(" ", end=' ')
    for j in range(cols):
        print(col_sums[j], end=' ')
    print()
    for i in range(rows):
        print(row_sums[i], end=' ')
        for j in range(cols):
            print("#" if x[i][j].Value() == 1 else ".", end=' ')
        print("")


if __name__ == "__main__":
    rows = [2, 2, 1, 1]
    cols = [1, 0, 3, 2]
    solve(rows, cols)
