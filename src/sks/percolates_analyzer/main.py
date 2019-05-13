import math
import random
import time

from sks.percolates_analyzer.percolation import UFDSQuickUnion, Percolation, UFDSQuickFind


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
        return sum(map(lambda xt: (xt - mean) ** 2, self.series_open_cell)) / (self.series_count - 1)

    def confidence(self):
        mean = self.mean()
        stddev = self.stddev()
        return mean - (1.96 * stddev) / math.sqrt(self.series_count), \
               mean + (1.96 * stddev) / math.sqrt(self.series_count)

    @staticmethod
    def _work(n, collection=UFDSQuickUnion):
        p = Percolation(n, collection)
        while not p.percolates():
            x, y = random.randrange(n), random.randrange(n)
            p.open(x, y)
        open_cells, close_cells = 0, 0
        for x in range(n):
            for y in range(n):
                if p.open(x, y):
                    open_cells += 1
                else:
                    close_cells += 1
        return open_cells, close_cells

    def do_experiment(self, n: int, series_count: int, collection=UFDSQuickUnion):
        if n <= 0 or series_count <= 0:
            raise ValueError
        self.series_open_cell = list()
        for _ in range(series_count):
            open_cells, close_cells = self._work(n, collection)
            self.series_open_cell.append(open_cells / close_cells)

    def __str__(self):
        return "mean\t=\t{0}\n" \
               "stddev\t=\t{1}\n" \
               "95% confidence interval\t=\t{2}".format(self.mean(), self.stddev(), str(self.confidence())[1:-1])


def main():
    in_n = int(input("n: "))
    in_count = int(input("count: "))
    in_collection = input("collection (qf or qu): ")
    t_collection = UFDSQuickFind if in_collection.strip().lower() == "qf" else UFDSQuickUnion
    ps = PercolationStats()
    before = time.perf_counter()
    ps.do_experiment(in_n, in_count, t_collection)
    print(str(ps))
    after = time.perf_counter()
    print(f"passsed {after - before} seconds")


if __name__ == '__main__':
    main()
