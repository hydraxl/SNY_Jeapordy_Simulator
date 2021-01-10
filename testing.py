def test_num_generator(n):
    def internal_generator():
        a = n
        while True:
            yield a
            a += 1
    g = internal_generator()
    return lambda: next(g)



a = test_num_generator(1)
print(a())
print(a())
