import random
import sys

# This may come in handy...
from fermat import miller_rabin

# If you use a recursive implementation of `mod_exp` or extended-euclid,
# you recurse once for every bit in the number.
# If your number is more than 1000 bits, you'll exceed python's recursion limit.
# Here we raise the limit so the tests can run without any issue.
# Can you implement `mod_exp` and extended-euclid without recursion?
sys.setrecursionlimit(4000)

# When trying to find a relatively prime e for (p-1) * (q-1)
# use this list of 25 primes
# If none of these work, throw an exception (and let the instructors know!)
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


# Implement this function
def ext_euclid(a: int, b: int) -> tuple[int, int, int]:
    """
    The Extended Euclid algorithm
    Returns x, y , d such that:
    - d = GCD(a, b)
    - ax + by = d

    Note: a must be greater than b
    """
    if b == 0:
        return 1, 0, a
    else:
        x1, y1, d = ext_euclid(b, a%b)
        x = y1 
        y = x1 - (a // b) * y1
        return x, y, d



# Implement this function
def generate_large_prime(bits=512) -> int:
    """
    Generate a random prime number with the specified bit length.
    Use random.getrandbits(bits) to generate a random number of the
     specified bit length.
    """
    while True:
        p = random.getrandbits(bits)
        if miller_rabin(p, 20) == "prime":
            return p


# Implement this function
def generate_key_pairs(bits: int) -> tuple[int, int, int]:
    p = generate_large_prime(bits // 2)
    q = generate_large_prime(bits // 2)
    N = p * q

    phi = (p - 1) * (q - 1)

    e = next(prime for prime in primes if ext_euclid(phi, prime)[2] == 1)  

    d, _, gcd = ext_euclid(e, phi)

    if gcd != 1:
        raise ValueError("e and phi are not coprime")

    d = d % phi
    
    return N, e, d

