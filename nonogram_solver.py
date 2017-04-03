#!/usr/bin/env python3
import argparse
from ortools.constraint_solver import pywrapcp
from timeit import default_timer as timer
import matplotlib.pyplot as plt
from dt_generator import *

def main(row_sums, col_sums, find_all=False, try_all_strat=False, print_sol=False, talk = True):
    # setting the strategies
    if try_all_strat:
        intvarstrategynameslist = ["CHOOSE_FIRST_UNBOUND", "CHOOSE_RANDOM", "CHOOSE_MIN_SIZE_LOWEST_MIN", "CHOOSE_MIN_SIZE_HIGHEST_MIN", "CHOOSE_MIN_SIZE_LOWEST_MAX", "CHOOSE_MIN_SIZE_HIGHEST_MAX", "CHOOSE_LOWEST_MIN", "CHOOSE_HIGHEST_MAX", "CHOOSE_MIN_SIZE", "CHOOSE_MAX_SIZE", "CHOOSE_PATH"]
        intvaluestrategynameslist = ["ASSIGN_MIN_VALUE", "ASSIGN_MAX_VALUE", "ASSIGN_RANDOM_VALUE", "ASSIGN_CENTER_VALUE", "SPLIT_LOWER_HALF", "SPLIT_UPPER_HALF"]
    else: 
        # default strategy
        intvarstrategynameslist = ["CHOOSE_FIRST_UNBOUND"]
        intvaluestrategynameslist = ["ASSIGN_MIN_VALUE"]

    # create a solver and compute solution with each configuration of strategies
    for varstrategy in intvarstrategynameslist:
        for valuestrategy in intvaluestrategynameslist:

            # initialization
            current_solver = pywrapcp.Solver("nonogram")
            n_rows = len(row_sums)
            n_cols = len(col_sums)

            # declare variables
            x = []
            for i in range(n_rows):
                t = []
                for j in range(n_cols):
                    t.append(current_solver.IntVar(0, 1, "x[%i,%i]" % (i, j)))
                x.append(t)
            x_flat = [x[i][j] for i in range(n_rows) for j in range(n_cols)]

            # constraints
            [current_solver.Add(current_solver.Sum([x[i][j] for j in range(n_cols)]) == row_sums[i]) for i in range(n_rows)]
            [current_solver.Add(current_solver.Sum([x[i][j] for i in range(n_rows)]) == col_sums[j]) for j in range(n_cols)]

            # solution and search
            solution = current_solver.Assignment()
            solution.Add(x_flat)

            # db: DecisionBuilder
            if talk:
                print("strategies:", varstrategy, valuestrategy)
            db = current_solver.Phase(x_flat, getattr(current_solver, varstrategy), getattr(current_solver, valuestrategy))
            current_solver.NewSearch(db)

            # find the solution(s)
            start = timer()
            if not find_all:  # if only one solution has to be printed
                current_solver.NextSolution()
                if print_sol:
                    print_solution(x, n_rows, n_cols, row_sums, col_sums)
            else:  # if all the solutions have to be printed
                num_solutions = 0
                while current_solver.NextSolution():
                    if print_sol:
                        print_solution(x, n_rows, n_cols, row_sums, col_sums)
                        print()
                    num_solutions += 1
                current_solver.EndSearch()
                print("num_solutions:", num_solutions)

            # print statistics about the resolution
            end = timer()
            if talk:
                print("failures:", current_solver.Failures())
                print("branches:", current_solver.Branches())
                print("WallTime:", current_solver.WallTime())
                print("{0:.3f}".format(end - start), "s", sep="")
                print("")

    if len(intvarstrategynameslist) == 1 and len(intvaluestrategynameslist):
        return (end - start)

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

def benchmark(find_all, try_all_strat, print_sol):
        times = []
        nb_element = []
        for i in range(100): 
            for j in range(10):
                pixs, row_sums, col_sums = pixs_to_dt(gen_random_pixs(j, j, .5))
                row_sums = row_sums.tolist()
                col_sums = col_sums.tolist()
                times.append(main(row_sums, col_sums, find_all, try_all_strat, print_sol, talk))
                nb_element.append(len(row_sums) * len(col_sums))
        plt.plot(nb_element, times, "ro")
        plt.ylabel('time')
        plt.xlabel('size')
        plt.show()

if __name__ == "__main__":
    # argparse definitions
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Path to the .txt representing the image')
    parser.add_argument('-a', action='store_true', help='Find all the solutions')
    parser.add_argument('-s', action='store_true', help='Try all strategies')
    parser.add_argument('-p', action='store_true', help='Print the solutions')
    parser.add_argument('-b', action='store_true', help='Start the benchmark')

    # argparse parsing
    args = parser.parse_args()
    path = args.path
    find_all = args.a
    try_all_strat = args.s
    print_sol = args.p
    start_bench = args.b

    # run main
    if start_bench:
        talk = False
        benchmark(find_all, try_all_strat, print_sol)

    elif path is not None:
        f = open(path, "r")
        row_sums = [int(r) for r in (f.readline().rstrip()).split(",")]
        col_sums = [int(c) for c in (f.readline().rstrip()).split(",")]
        main(row_sums, col_sums, find_all, try_all_strat, print_sol)
        print("Path:", path)
