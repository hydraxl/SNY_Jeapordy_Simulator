class N:
    def __init__(self):
        self.n = 0

a = [N() for i in range(3)]
b = [N()]*3
a[0].n = 1
b[0].n = 1
print([i.n for i in a])
print([i.n for i in b])
