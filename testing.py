seq_gen = lambda seq: [(yield seq[i]) for i in range(len(seq))]
a = seq_gen([10 - i for i in range(10)])
for i in range(10): print(next(a))
