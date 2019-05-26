"""
This module provides statistical methods for time performance.
"""
import time
from itertools import product

from sks.percolatesanalyzer.main import PercolationStats
from sks.percolatesanalyzer.percolation import UFDSQuickFind, UFDSQuickUnion

__author__ = "6rayWa1cher"


def start_process(collection):
    n_arr = [5 * (2 ** i) for i in range(4)]
    cycles_arr = [50 * (10 ** i) for i in range(3)]
    ps = PercolationStats()
    for n, cycles in product(n_arr, cycles_arr):
        print("Starting n:{0} cycles:{1} test...".format(n, cycles), end=' ')
        before = time.perf_counter()
        ps.do_experiment(n, cycles, collection)
        after = time.perf_counter()
        print(f"passsed {after - before} seconds")


if __name__ == '__main__':
    in_collection = input("collection (qf or qu): ")
    t_collection = UFDSQuickFind if in_collection.strip().lower() == "qf" else UFDSQuickUnion
    start_process(t_collection)
