#!/usr/bin/env python3
from custom_solver_4 import solve as custom_solve
from or_tools_solver import solve as or_tools_solve
from timeit import default_timer as timer


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



import sys
import dt_generator
sys.setrecursionlimit(1024*1024*2)


for i in range(32):
    dim = i * 4

    pixs, rows, cols = dt_generator.pixs_to_dt(dt_generator.gen_random_pixs(dim, dim, .5))
    rows = rows.tolist()
    cols = cols.tolist()

    start = timer()
    custom_solve(rows, cols)
    print("dim: ", dim)
    print("CUSTOM SOLVER: ", "{0:.3f}".format(timer() - start), "s", sep="")
    start = timer()
    or_tools_solve(rows, cols)
    print("OR-TOOLS SOLVER: ", "{0:.3f}".format(timer() - start), "s", sep="")
    print()
