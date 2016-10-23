from __future__ import unicode_literals, absolute_import

import hashlib
from random import randint


def module_pow(x, y, m):
    """Calculate x^y (mod m)
    :type x: int
    :type y: int
    :type m: int
    :rtype: int
    """
    if y == 0:
        return 1

    result = module_pow(x, y / 2, m)
    result = result * result % m

    if y % 2 == 1:
        result = (result * x) % m

    return result


def is_simple(n):
    """Check if n is prime
    :param n: number > 2
    :type n: int
    :rtype: bool
    """
    assert n > 2
    if n % 2 == 0:
        return False

    k = 50

    s = 0
    t = n - 1
    while t % 2 == 0:
        t /= 2
        s += 1

    for _ in xrange(k):
        a = randint(2, n - 2)
        x = module_pow(a, t, n)

        if x == 1 or x == n - 1:
            continue

        for _ in xrange(s - 1):
            x = x * x % n

            if x == 1:
                return False, 1

            if x == n - 1:
                break

        if x == n - 1:
            continue

        return False, 0, x

    return True


def get_hash(number):
    """Return int hash of int number
    :type number: int
    :rtype: int
    """
    bits_squence = bin(number)[2:]
    string_result = hashlib.sha1(bits_squence).hexdigest()
    result = int(string_result, base=16)
    return result


def generate(n, l):
    """Return 2 simple numbers p and q
    :param n: bits count in p
    :type n: int
    :param l: bits count in q
    :type l: int
    :return: (p, q)
    :rtype: tuple
    """
    n_little = (l - 1) / n
    b = (l - 1) % n
    p = 0
    q = 0

    while True:

        # steps 1 - 6
        seed = 0
        seedlen = n + 1

        for i in xrange(seedlen):
            seed = seed * 2 + randint(0, 1)

        u = get_hash(seed) ^ get_hash((seed + 1) % 2**seedlen)

        q = 2 ** (n - 1) | 1 | u

        if not is_simple(q):
            continue

        counter = 0
        offset = 2

        # steps 7 - ..
        while True:
            v = []

            for k in xrange(n_little + 1):
                v.append(
                    get_hash((seed + offset + k) % 2**seedlen)
                )

            w = sum(v[i] * 2**(n * i) for i in xrange(n_little))
            w += (v[n_little] % b) * 2 ** (n_little * n)

            x = w + 2 ** (l - 1)

            c = x % (2 * q)
            p = x - (c - 1)

            if p < 2 ** (l - 1):
                # steps 13 and 14

                counter += 1
                offset += n_little + 1

                if counter > 2 ** 12:
                    break
                else:
                    continue

            if is_simple(p):
                break

        if counter > 2 ** 12:
            continue

        if is_simple(p):
            break

    return q, p


if __name__ == '__main__':
    print generate(20, 32)