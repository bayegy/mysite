class Test(object):
    """docstring for Test"""

    def __init__(self):
        self.y1 = self.ty()

    def ty(self):
        while True:
            try:
                for i in [1, 2, 3]:
                    yield(i)
            except Exception as e:
                print(e)
                self.y1 = self.ty()
                while True:
                    yield(self.y1.__next__())
