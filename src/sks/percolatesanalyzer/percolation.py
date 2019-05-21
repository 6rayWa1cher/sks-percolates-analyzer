class UFDSQuickFind:
    def __init__(self, n=0):
        self.st = [i for i in range(n)]
        self.ln = n

    def union_set(self, x, y):
        curr_set = self.st[y]
        for i in range(self.ln):
            if self.st[i] == curr_set:
                self.st[i] = self.st[x]

    def find_set(self, x):
        return self.st[x]

    def connected(self, x, y):
        return self.st[x] == self.st[y]

    def __str__(self):
        return " ".join(map(str, self.st))


class UFDSQuickUnion:
    def __init__(self, N=0):
        self._rank = [0 for _ in range(N)]
        self._id = [i for i in range(N)]
        self.ln = N

    def union_set(self, x, y):
        py = self.root(y)
        px = self.root(x)
        if py == px:
            return
        if self._rank[py] > self._rank[px]:
            px, py = py, px
        self._id[py] = px
        self._rank[px] = max(self._rank[px], self._rank[py] + 1)

    def root(self, x):
        temp = self._id[x]
        passed = []
        while not temp == self._id[temp]:
            passed.append(temp)
            temp = self._id[temp]
        for u in passed + [x]:
            self._id[u] = temp
        return temp

    def connected(self, x, y):
        return self.root(x) == self.root(y)

    def set_count(self):
        temp = set()
        for u in self._id:
            if u not in temp:
                temp.add(u)
        return len(temp)

    def __str__(self):
        return " ".join(map(lambda x: str(x[0]) if type(x) is list else str(x), self._id)) + "\n" + " ".join(
            map(str, self._rank))


class Percolation:
    def __init__(self, n, uf=UFDSQuickUnion):
        self.n = n
        self.mass = [[0 for i in range(n)] for j in range(n)]
        self.field = uf(n ** 2 + 2)
        for i in range(n):
            self.field.union_set(0, i + 1)
            self.field.union_set(n ** 2 + 1, n ** 2 - i)

    def getfindex(self, i, j):
        return 1 + (i * self.n) + j

    def is_open(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return False
        return self.mass[i][j] == 1

    def open(self, i, j):
        self.mass[i][j] = 1
        if self.is_open(i - 1, j):
            self.field.union_set(self.getfindex(i, j), self.getfindex(i - 1, j))
        if self.is_open(i + 1, j):
            self.field.union_set(self.getfindex(i, j), self.getfindex(i + 1, j))
        if self.is_open(i, j - 1):
            self.field.union_set(self.getfindex(i, j), self.getfindex(i, j - 1))
        if self.is_open(i, j + 1):
            self.field.union_set(self.getfindex(i, j), self.getfindex(i, j + 1))

    def is_full(self, i, j):
        return self.field.connected(0, self.getfindex(i, j))

    def percolates(self):
        return self.field.connected(0, (self.n ** 2) + 1)

    def __str__(self):
        ret = ""
        ret += "Array:\n"
        for u in self.mass:
            ret += (" ".join(map(str, u)) + "\n")
        ret += "UFDS\n"
        ret += str(self.field)
        return ret
