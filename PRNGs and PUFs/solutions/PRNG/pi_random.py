import time

def pi_bbp():
    """Conjectured BBP generator of hex digits of pi."""
    # https://possiblywrong.wordpress.com/2017/09/30/digits-of-pi-and-python-generators/
    a, b = 0, 1
    k = 0
    while True:
        ak, bk = (120 * k**2 + 151 * k + 47,
                  512 * k**4 + 1024 * k**3 + 712 * k**2 + 194 * k + 15)
        a, b = (16 * a * bk + ak * b, b * bk)
        digit, a = divmod(a, b)
        yield digit
        k = k + 1

def random_bits():
    for digit in pi_bbp():
        for i in range(4):
            yield (digit >> i) & 1

prev_time = time.time()

for bit, i in zip(random_bits(), range(1000000)):
    if i % 10000 == 0:
        new_time = time.time()
        print(new_time-prev_time)
        prev_time = new_time