"""
Provides PercolationStats and main runner

PercolationStats holds experiment stats, and defines Monte-Carlo
logic.
"""
import random
import time
from multiprocessing import Pipe, connection, Process

import math

from sks.percolatesanalyzer.percolation import UFDSQuickUnion, Percolation, UFDSQuickFind

__author__ = "6rayWa1cher"


class PercolationStats:
    def __init__(self):
        self.series_open_cell = list()

    @property
    def series_count(self):
        return len(self.series_open_cell)

    def mean(self):
        return sum(self.series_open_cell) / self.series_count

    def stddev(self):
        mean = self.mean()
        return math.sqrt(sum(map(lambda xt: (xt - mean) ** 2, self.series_open_cell)) / (self.series_count - 1))

    def confidence(self):
        mean = self.mean()
        stddev = self.stddev()
        return mean - (1.96 * stddev) / math.sqrt(self.series_count), \
               mean + (1.96 * stddev) / math.sqrt(self.series_count)

    @staticmethod
    def _work(n, collection=UFDSQuickUnion):
        """
        Single work for Monte-Carlo experiment.
        Opens cells until matrix percolates then count open and closed cells.
        :param n: size of matrix (n x n)
        :param collection: UFDS, see `sks.percolatesanalyzer.percolation.Percolation`
        :return: a tuple with the number of open and closed cells.
        """
        p = Percolation(n, collection)
        while not p.percolates():
            y, x = random.randrange(n), random.randrange(n)
            p.open(y, x)
        open_cells, close_cells = 0, 0
        for y in range(n):
            for x in range(n):
                if p.is_open(y, x):
                    open_cells += 1
                else:
                    close_cells += 1
        return open_cells, close_cells

    def do_experiment(self, n: int, series_count: int, collection=UFDSQuickUnion):
        """
        Runs Monte-Carlo experiment (single-thread mode)
        :param n: size of matrix (n x n)
        :param series_count: number of Monte-Carlo series
        :param collection: UFDS, see `sks.percolatesanalyzer.percolation.Percolation`
        :return: None
        """
        if n <= 0 or series_count <= 0:
            raise ValueError
        self.series_open_cell = list()
        for _ in range(series_count):
            open_cells, close_cells = self._work(n, collection)
            self.series_open_cell.append(open_cells / (close_cells + open_cells))

    def _do_parallel_experiment(self, n, collection, pipe: connection.Connection, times):
        """
        Single thread logic of Monte-Carlo multi-thread experiment
        :param n: size of matrix (n x n)
        :param collection: UFDS, see `sks.percolatesanalyzer.percolation.Percolation`
        :param pipe: connection between main runner and this thread
        :param times: number of Monte-Carlo series (for this thread)
        :return: None
        """
        buffer = list()
        for _ in range(times):
            open_cells, close_cells = self._work(n, collection)
            buffer.append(open_cells / (close_cells + open_cells))
        pipe.send(buffer)

    def do_parallel_experiment(self, n: int, series_count: int, threads=8, collection=UFDSQuickUnion):
        """
        Runs Monte-Carlo experiment (multi-thread mode)
        :param n: size of matrix (n x n)
        :param series_count: number of Monte-Carlo series
        :param threads: number of processes, which will be created for experiments
        :param collection: UFDS, see `sks.percolatesanalyzer.percolation.Percolation`
        :return: None
        """
        if n <= 0 or series_count <= 0 or threads <= 0:
            raise ValueError
        self.series_open_cell = list()
        parent_conn, child_conn = Pipe()
        processes = list()
        assigned_series_count = 0
        for _ in range(threads - 1):
            curr_series_count = series_count // threads
            p = Process(target=self._do_parallel_experiment, args=(n, collection, child_conn, curr_series_count))
            assigned_series_count += curr_series_count
            processes.append(p)
            p.start()
        p = Process(target=self._do_parallel_experiment,
                    args=(n, collection, child_conn, series_count - assigned_series_count))
        processes.append(p)
        p.start()
        for _ in range(threads):
            buffer = parent_conn.recv()
            self.series_open_cell += buffer
        for p in processes:
            p.join()

    def __str__(self):
        return "mean\t=\t{0}\n" \
               "stddev\t=\t{1}\n" \
               "95% confidence interval\t=\t{2}".format(self.mean(), self.stddev(), str(self.confidence())[1:-1])


def main():
    in_n = int(input("n: "))
    in_count = int(input("count: "))
    in_collection = input("collection (qf or qu): ")
    in_threads = int(input("parallel_processes (1 for single thread): "))
    t_collection = UFDSQuickFind if in_collection.strip().lower() == "qf" else UFDSQuickUnion
    ps = PercolationStats()
    before = time.perf_counter()
    if in_threads != 1:
        ps.do_parallel_experiment(in_n, in_count, collection=t_collection)
    else:
        ps.do_experiment(in_n, in_count, t_collection)
    print(str(ps))
    after = time.perf_counter()
    print(f"passsed {after - before} seconds")


if __name__ == '__main__':
    main()
