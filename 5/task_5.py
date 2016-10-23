from __future__ import unicode_literals, absolute_import

import collections
from random import randint


KEY_FILE = 'key.txt'


def is_prime(n):
    """Check if n is prime
    :param n: number > 2
    :type n: int
    :rtype: bool
    """
    if n == 2:
        return True

    if n < 2:
        return False

    k = 50

    s = 0
    t = n - 1
    while t % 2 == 0:
        t /= 2
        s += 1

    for _ in xrange(k):
        a = randint(2, max(n - 2, 2))
        x = pow(a, t, n)

        if x == 1 or x == (n - 1):
            continue

        for _ in xrange(s - 1):
            x = pow(x, 2, n)

            if x == 1:
                return False

            if x == n - 1:
                break

        if x == n - 1:
            continue

        return False

    return True

def read_key():
    with open(KEY_FILE, 'r') as f:
        key = int(f.readline(), base=16)

    return key


def find_simple(number):
    """Find prime which greater than number.
    :type number: int
    :rtype: int
    """
    number += 1
    while not is_prime(number):
        number += 1

    return number


def find_gcd(a, b):
    """
    :type a: int
    :type b: int
    :rtype: int
    """
    while a > 0 and b > 0:
        if a > b:
            a %= b
        else:
            b %= a

    return a + b


def find_relatively_prime(prime, count):
    """Return count relatively primes which greater than prime.
    :type prime: int
    :type count: int
    :rtype: list
    """
    result = []
    current = prime + 1
    result.append(current)

    lcm = current
    while len(result) < count:
        current += 1

        if find_gcd(lcm, current) != 1:
            continue

        result.append(current)
        lcm *= current

    return result


def encode(n, m, key):
    assert 3 < n < 20, 'Wrong participants count'
    assert 2 < m < 19 and m < n, 'Wrong key participants count'

    p = find_simple(key)

    relatively_primes = find_relatively_prime(p, n)

    high_border = 1
    for i in xrange(m):
        high_border *= relatively_primes[i]

    low_border = 1
    for i in xrange(m - 1):
        low_border *= relatively_primes[n - i - 1]

    r = (high_border - key - 1) / p

    upgraded_secret = key + r * p

    parts = [
        (p, item, upgraded_secret % item)
        for item in relatively_primes
    ]

    return parts


### DECODE


def euler(number):
    """Return value of Euler's function for number
    :type number: int
    :rtype: int
    """
    values = collections.defaultdict(lambda: 0)

    for i in xrange(2, int(number ** 0.5) + 1):
        while number % i == 0:
            values[i] += 1
            number /= i

    values[number] += 1
    values.pop(1, 0)

    result = 1
    for divisor, count in values.items():
        result *= (divisor - 1) * (divisor ** (count - 1))

    return result


def get_upgraded_secret(a, p):
    """Return X according to chinese remainder theorem.
    :param a: remainders
    :type a: list
    :param p: modules
    :type p: list
    :rtype: int
    """
    assert len(a) == len(p)
    k = len(p)

    x = [0 for _ in a]
    r = [
        [0 for _ in xrange(k)]
        for _ in xrange(k)
    ]

    for i in xrange(k - 1):
        for j in xrange(i + 1, k):
            eu = euler(p[j]) - 1
            r[i][j] = eu

    for i in xrange(k):
        x[i] = a[i]
        for j in xrange(i):
            x[i] = r[j][i] * (x[i] - x[j])

            x[i] = x[i] % p[i]
            if (x[i] < 0): x[i] += p[i]

    ans = 0
    for i in xrange(k):
        mult = x[i]
        for j in xrange(i):
            mult *= p[j]

        ans += mult

    return ans


def decode(parts):
    upgraded_secret = get_upgraded_secret(
        [item[2] for item in parts],
        [item[1] for item in parts],
    )

    secret = upgraded_secret % parts[0][0]

    with open('out.txt', 'w') as f:
        f.write(hex(secret))



### MAIN

if __name__ == '__main__':
    key = read_key()
    n = 4
    m = 3
    parts = encode(n, m, key)

    with open('parts.txt', 'w') as f:
        for item in parts:
            f.write(str(item) + '\n')

    decode(parts[:m])
