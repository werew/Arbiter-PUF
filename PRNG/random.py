class Random(object):
    def __init__(self):
        self.seed([1, 2, 3, 4])

    def seed(self, state):
        self.state = state

    def iter_bits(self):
        while True:
            self.state = self.xorshift128(self.state)
            yield self.state[0] & 1

    def xorshift128(self, state_):
        # https://en.wikipedia.org/wiki/Xorshift
        state = state_[:]
        s = t = state[3]
        t ^= (t << 11) & 0xffffffff
        t ^= (t >> 8) & 0xffffffff
        state[3] = state[2]
        state[2] = state[1]
        state[1] = s = state[0]
        t ^= s
        t ^= (s >> 19) & 0xffffffff
        state[0] = t
        return state

random = Random()

take = lambda iterator, n: [x for x, _ in zip(iterator, range(n))]

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

with open('random_bits', 'wb') as f:
    for bs in chunks(take(random.iter_bits(), 1028016), 8):
        f.write(bytes([int(''.join(str(b) for b in bs), 2)]))

