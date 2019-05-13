class UFDSQF:
    def __init__(self, N=0):
        self.st = [i for i in range(N)]
        self.ln = N

    def union_set(self, x, y):
        currset = self.st[y]
        for i in range(self.ln):
            if self.st[i] == currset:
                self.st[i] = self.st[x]

    def find_set(self, x):
        return self.st[x]

    def connected(self, x, y):
        return self.st[x] == self.st[y]

    def __str__(self):
        return " ".join(map(str, self.st))


class UFDSQU:
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
    def __init__(self, N=None, uf=UFDSQU):
        self.uf = uf
        self.mass = None
        self.field = None
        self.N = N
        if str(N).isnumeric():
            self.Percolation(N)

    def Percolation(self, N):
        self.mass = [[0 for _ in range(N)] for _ in range(N)]
        self.field = self.uf(N ** 2 + 2)
        self.N = N
        for i in range(N):
            self.field.union_set(N ** 2, i)
            self.field.union_set(N ** 2 + 1, N ** 2 - 1 - i)

    def open(self, i, j):
        self.mass[i][j] = 1
        try:
            if self.isOpen(i - 1, j):
                self.field.union_set(self.N * i + j, self.N * (i - 1) + j)
        except IndexError:
            pass
        try:
            if self.isOpen(i + 1, j):
                self.field.union_set(self.N * i + j, self.N * (i + 1) + j)
        except IndexError:
            pass
        try:
            if self.isOpen(i, j - 1):
                self.field.union_set(self.N * i + j, self.N * i + (j - 1))
        except IndexError:
            pass
        try:
            if self.isOpen(i, j + 1):
                self.field.union_set(self.N * i + j, self.N * i + (j + 1))
        except IndexError:
            pass

    def isOpen(self, i, j):
        return self.mass[i][j] == 1

    def isFull(self, i, j):
        return self.field.connected(i * self.N + j, self.N ** 2)

    def percolates(self):
        return self.field.connected(self.N ** 2, self.N ** 2 + 1)

    def __str__(self):
        ret = ""
        ret += "Array:\n"
        for u in self.mass:
            ret += (" ".join(map(str, u)) + "\n")
        ret += "UFDS\n"
        ret += str(self.field)
        return ret


"""
print("UFDSQU", "\n")
per = Percolation(4)
print(per, "\n")
per.open(0, 0)
print(per, "\n")
per.open(1, 0)
print("per.isOpen(1, 0)", per.isOpen(1, 0), "\n")
print("per.isOpen(1, 1)", per.isOpen(1, 1), "\n")
print("per.isFull(1, 0)", per.isFull(1, 0), "\n")
print("per.isFull(1, 1)", per.isFull(1, 1), "\n")
per.open(2, 0)
print("percolates()", per.percolates(), "\n")
per.open(3, 0)
print(per, "\n")
print("percolates()", per.percolates(), "\n")
print("UFDSQF", "\n")
per = Percolation(4, UFDSQF)
print(per, "\n")
per.open(0, 0)
print(per, "\n")
per.open(1, 0)
print("per.isOpen(1, 0)", per.isOpen(1, 0), "\n")
print("per.isOpen(1, 1)", per.isOpen(1, 1), "\n")
print("per.isFull(1, 0)", per.isFull(1, 0), "\n")
print("per.isFull(1, 1)", per.isFull(1, 1), "\n")
per.open(2, 0)
print("percolates()", per.percolates(), "\n")
per.open(3, 0)
print(per, "\n")
print("percolates()", per.percolates(), "\n")
"""
