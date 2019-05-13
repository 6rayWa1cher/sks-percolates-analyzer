import src.sks.percolates_analyzer.percolation as fortest


class TestUFDSQF:
    def setup_method(self, method):
        self.UFDS = fortest.UFDSQuickFind(3)

    def teardown_method(self, method):
        self.UFDS = None

    def test_find_set(self):
        x = self.UFDS.st[0]
        assert self.UFDS.find_set(0) == x
        x = self.UFDS.st[1]
        assert self.UFDS.find_set(1) == x

    def test_union_set(self):
        assert self.UFDS.st[0] == 0
        assert self.UFDS.st[1] == 1
        self.UFDS.union_set(0, 1)
        assert self.UFDS.st[1] == self.UFDS.st[0]

    def test_connected(self):
        assert not (self.UFDS.st[0] == self.UFDS.st[1])
        assert not (self.UFDS.connected(0, 1))
        self.UFDS.union_set(0, 1)
        assert (self.UFDS.st[0] == self.UFDS.st[1])
        assert (self.UFDS.connected(0, 1))


class TestUFDSQU:
    def setup_method(self, method):
        self.UFDS = fortest.UFDSQuickUnion(3)

    def teardown_method(self, method):
        self.UFDS = None

    def test_union_set(self):
        assert self.UFDS._id[0] == 0
        assert self.UFDS._id[1] == 1
        self.UFDS.union_set(0, 1)
        assert self.UFDS._id[1] == self.UFDS._id[0]

    def test_connected(self):
        assert not (self.UFDS._id[0] == self.UFDS._id[1])
        assert not (self.UFDS.connected(0, 1))
        self.UFDS.union_set(0, 1)
        assert (self.UFDS._id[0] == self.UFDS._id[1])
        assert (self.UFDS.connected(0, 1))


class TestPercolation:
    def setup_method(self, method):
        self.per = fortest.Percolation(4)

    def teardown_method(self, method):
        self.per = None

    def test_open(self):
        assert self.per.mass[0][0] == 0
        self.per.open(0, 0)
        assert self.per.mass[0][0] == 1
        assert not self.per.field.connected(1, 5)
        assert self.per.mass[1][0] == 0
        self.per.open(1, 0)
        assert self.per.mass[1][0] == 1
        assert self.per.field.connected(1, 5)

    def test_isOpen(self):
        assert not self.per.is_open(1, 0)
        self.per.open(1, 0)
        assert self.per.is_open(1, 0)

    def test_isFull(self):
        assert not self.per.is_full(1, 0)
        self.per.open(0, 0)
        assert not self.per.is_full(1, 0)
        self.per.open(1, 0)
        assert self.per.is_full(1, 0)

    def test_percolates(self):
        assert not self.per.percolates()
        self.per.open(0, 0)
        assert not self.per.percolates()
        self.per.open(1, 0)
        assert not self.per.percolates()
        self.per.open(2, 0)
        assert not self.per.percolates()
        self.per.open(3, 0)
        assert self.per.percolates()


class TestPercolation2:
    def setup_method(self, method):
        self.per = fortest.Percolation(4, fortest.UFDSQuickFind)

    def teardown_method(self, method):
        self.per = None

    def test_open(self):
        assert self.per.mass[0][0] == 0
        self.per.open(0, 0)
        assert self.per.mass[0][0] == 1
        assert not self.per.field.connected(1, 5)
        assert self.per.mass[1][0] == 0
        self.per.open(1, 0)
        assert self.per.mass[1][0] == 1
        assert self.per.field.connected(1, 5)

    def test_isOpen(self):
        assert not self.per.is_open(1, 0)
        self.per.open(1, 0)
        assert self.per.is_open(1, 0)

    def test_isFull(self):
        assert not self.per.is_full(1, 0)
        self.per.open(0, 0)
        assert not self.per.is_full(1, 0)
        self.per.open(1, 0)
        assert self.per.is_full(1, 0)

    def test_percolates(self):
        assert not self.per.percolates()
        self.per.open(0, 0)
        assert not self.per.percolates()
        self.per.open(1, 0)
        assert not self.per.percolates()
        self.per.open(2, 0)
        assert not self.per.percolates()
        self.per.open(3, 0)
        assert self.per.percolates()
