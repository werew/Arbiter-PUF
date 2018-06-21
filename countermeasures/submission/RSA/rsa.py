import math

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def int_to_bits(x):
    """Converts a number to a bit list"""
    bits = []
    while x > 0:
        bits.append(x & 1)
        x >>= 1
    return bits

def square_and_multiply(m, n, d):
    """Computes (m^d) mod n"""
    d = int_to_bits(d)
    a = 1
    for i in reversed(range(0, len(d))):
        a = (a**2) % n
        if d[i] == 1: a = (a*m) % n
    return a

def square_and_multiply_always(m, n, d):
    """Computes (m^d) mod n"""
    d = int_to_bits(d)
    R = [1, m]
    i, t = len(d) - 1, 0
    while i >= 0:
        R[0] = (R[0] * R[t]) % n
        t = (t ^ d[i])
        i = i - 1 + t
    return R[0]

def montgomery_ladder(m, n, d):
    """Computes (m^d) mod n"""
    d = int_to_bits(d)
    R = [1, m]
    for i in reversed(range(0, len(d))):
        R[1-d[i]] = (R[0]*R[1]) % n
        R[d[i]] = (R[d[i]]**2) % n
    return R[0]

# sample RSA parameters
p, q = 953, 997
n = p*q
e = 65537
d = modinv(e, (p-1)*(q-1))

methods = [
    ('square and multiply', square_and_multiply),
    ('square and multiply always', square_and_multiply_always),
    ('montgomery ladder', montgomery_ladder)
]

for (name, method) in methods:
    print('[+] Testing {} method'.format(name))

    # check encryption and decryption of various messages
    for m in range(100):
        assert(method(method(m, n, e), n, d) == m)

