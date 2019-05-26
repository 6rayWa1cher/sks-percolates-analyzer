"""
This module provides statistical methods for the confidence interval, graphics builder.
"""
from itertools import product
from typing import Mapping, Iterable, Tuple, NewType

import matplotlib.pyplot as plt

from sks.percolatesanalyzer.main import PercolationStats
from sks.percolatesanalyzer.percolation import UFDSQuickUnion

__author__ = "6rayWa1cher"

border_type = NewType("borders", Mapping[int, Iterable[Tuple[int, int, int]]])


def start_process(n_arr, cycles_arr, vibration_factor=3, primary_key_cycles=False) -> border_type:
    """
    Runs various Monte-Carlo experiments and return its results in dict.
    Vibration factor defines how many times each experiment configuration
    will be run. Only the average result will be taken into account
    (by the mean value of the interval).
    :param n_arr: array of matrix sizes (n x n)
    :param cycles_arr: array of cycles
    :param vibration_factor: how many times each config will be run
    :param primary_key_cycles: is cycle - primary key
    :return: n -> set( (cycle, left, right) ) if not primary_key_cycles, else
        cycle -> set( (n, left, right) )
    """
    ps = PercolationStats()
    if primary_key_cycles:
        borders = {c: set() for c in cycles_arr}
    else:
        borders = {n: set() for n in n_arr}
    for n, cycles in product(n_arr, cycles_arr):
        print("Starting n:{0} cycles:{1} test...".format(n, cycles), end=' ')
        curr_borders = list()
        for _ in range(vibration_factor):
            # If the test in single-thread mode takes lower than one second on the test stand,
            # it will better start single-thread mode. The formula is derived by testing.
            if (10 ** -2) * ((n / 5) ** 2) * (cycles / 50) > 1.0:
                ps.do_parallel_experiment(n, cycles, threads=8, collection=UFDSQuickUnion)
            else:
                ps.do_experiment(n, cycles, UFDSQuickUnion)
            l, r = ps.confidence()
            curr_borders.append(((l + r) / 2, l, r))
        center_index = len(curr_borders) // 2
        curr_borders.sort()
        _, l, r = curr_borders[center_index]
        if primary_key_cycles:
            borders[cycles].add((n, l, r))
        else:
            borders[n].add((cycles, l, r))
        print("interval {0}, {1}".format(l, r))
    return borders


def draw_graphics(borders: border_type, primary_key_cycles=False):
    """
    Draw graphics on display
    :param borders: see start_process return
    :param primary_key_cycles: is cycle - primary key
    :return: None
    """
    fig, axs = plt.subplots(nrows=len(borders.keys()), ncols=2)
    i = 0
    for primary, lr_set in borders.items():
        ax_arr = axs[i]
        ax = ax_arr[0]
        i += 1
        keys = list()
        left = list()
        right = list()
        delta = list()
        center = list()
        for secondary, l, r in sorted(lr_set):
            keys.append(secondary)
            left.append(l)
            right.append(r)
            delta.append(r - l)
            center.append((l + r) / 2)
        ax.plot(keys, left, label="left")
        ax.plot(keys, right, label="right")
        ax.plot(keys, center, label='center')
        ax.set_ylabel('Confidence border')
        ax.set_xlabel('n' if primary_key_cycles else 'Cycles')
        ax.set_title(('cycles = {0}' if primary_key_cycles else 'n = {0}').format(primary))
        ax.legend(loc='lower right')
        ax.grid(True)
        ax = ax_arr[1]
        ax.plot(keys, delta)
        ax.set_xlabel('n' if primary_key_cycles else 'Cycles')
        ax.set_ylabel('Delta')
        ax.grid(True)
    plt.subplots_adjust(left=0.08, bottom=0.11, right=0.96, top=0.96, wspace=0.2, hspace=0.5)
    fig.set_size_inches(6.4 * 1.5, 4.8 * 1.5)
    plt.show()


if __name__ == '__main__':
    # primary - n, secondary - cycles
    draw_graphics(start_process([5, 10], list(range(50, 5000, 200))))
    # primary - cycles, secondary - n
    draw_graphics(start_process(list(range(5, 50)), [500, 5000], primary_key_cycles=True), True)
