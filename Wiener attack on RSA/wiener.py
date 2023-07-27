from random import randint, choice
from math import gcd
from sympy import *
import numpy as np


def generate_large_prime_number(low, high):
    return randprime(low, high)


def calculate_eulerian(num):
    """
        number of elements in `Reduced Set of Residues` of `num` which doesn't have common divisor with `num`
    """
    if num == 1:
        return 1
    else:
        n = [i for i in range(1, num) if gcd(num, i) == 1]
        return len(n)


def generate_public_key(phi, private_key):
    """
        ed = 1 mod phi(n) --> e = d^-1 mod phi(n)
    """
    try:
        return pow(private_key, -1, phi)
    except ValueError:
        return False


def continued_fraction(n, d):
    """
        Compute the continued fraction expansion of n/d
        this expansion gives us the value to reach n/d.
        example : n = 45, d = 13 --> returns [3, 2, 6], as we know 45/13 is almost 3.46
        45 / 13 = 3 + (1 / (2 + ( 1/6)))
    """
    expansion = []
    while d != 0:
        expansion.append(n // d)
        n, d = d, n % d
    return expansion


def compute_convergents(coefficients):
    """
        params : coefficients --> continued fraction coefficient
        returns approximate(convergent of this coefficient at each step) --> the more it reaches to end the closer are
        number to nominator and denominator
        computes until each element what is value of fraction
        for example just like example before:
        coefficients : [3, 2, 6] --> returns  [    3 ,     3 + 1/2    ,    3 + 1 / (2 + 1/6)]
    """
    if len(coefficients) == 1:
        return [(coefficients[0], 1)]

    convergents = []
    n0, n1 = coefficients[0], coefficients[0] * coefficients[1] + 1  # Initial numerator values
    d0, d1 = 1, coefficients[1]  # Initial denominator values
    convergents.append((n0, d0))
    convergents.append((n1, d1))

    for i in range(2, len(coefficients)):
        p = coefficients[i] * convergents[i - 1][0] + convergents[i - 2][
            0]  # Compute the numerator of the next convergent
        q = coefficients[i] * convergents[i - 1][1] + convergents[i - 2][
            1]  # Compute the denominator of the next convergent
        convergents.append((p, q))  # Append the convergent to the list

    return convergents


def create_primes(low, high):
    p = generate_large_prime_number(low, high)  # generate large prime number between low and high
    q = generate_large_prime_number(low, high)  # generate large prime number between low and high

    while not (q < p < 2 * q):  # loop until condition met
        p = generate_large_prime_number(low, high)
        q = generate_large_prime_number(low, high)
    print(f"p : {p}, q : {q}")
    N = p * q
    phi_N = (p - 1) * (q - 1)

    return N, phi_N


def generate_d_possible_values(n):
    max_value = (1 / 3) * (n ** (1 / 4))  # based on the fact that d < 1/3 n^1/4
    print(f"max value d can get is {max_value}")
    return [i for i in list(range(2, int(max_value))) if i % 2 != 0]


def create_rsa_variables():
    low_num = 1e5
    high_num = 1e7

    N, phi_N = create_primes(low_num, high_num)

    d_possible_values = generate_d_possible_values(N)
    d = choice(d_possible_values)
    e = generate_public_key(phi_N, d)
    while not e:  # regenerating if condition on `e` and `d` didn't held
        d_possible_values.remove(d)
        if len(d_possible_values) == 0:
            print("d can't get value from this range we should set another p, q again")
            N, phi_N = create_primes(low_num, high_num)
            d_possible_values = generate_d_possible_values(N)
        d = choice(d_possible_values)
        e = generate_public_key(phi_N, d)

    print()

    print(f"N : {N}")
    print(f"phi_N : {phi_N}")
    print(f"public key : {e}")
    print(f"private key : {d}")
    if (e * d) % phi_N == 1:
        print("e and d are inverse modulo in mod phi_N")

    m = randint(5, 1200)
    ci = pow(m, e, N)
    deciphered = pow(ci, d, N)
    if m == deciphered:
        print("keys are correctly set")
    else:
        print("key's aren't correct")
        assert False

    return N, phi_N, e, d


def Wiener_attack():
    """
        this attack works as follows:
        e/n convergents may contains k/d in itself. so if we have k and d we can get value of φ
        φ = (ed - 1) / k, after that if we have φ, we can solve polynomial equation
        "p^2 + p(φ(n) - n - 1) + n = 0" and this equation shows us n = p1.p2 --> n = p.q , so we check if p1 x p2 = n
        then we have p and q and our private key is correct
    """
    N, phi_N, e, d = create_rsa_variables()

    # pq = n
    # ed - kφ(n) = 1
    # φ(n) = (p-1)(q-1) = pq - p - q + 1 = n - p - q + 1 --> p and q are much smaller than n --> φ(n) ≈ n
    # ed ≈ kn --> e/n ≈ k/d
    # because the upper formula are approximately equal; so if we search for convergents of e/n we can possibly
    # find the correct value of k/d. there is a chance that `ith` convergent of e/n is exactly k/d
    coeffs = continued_fraction(e, N)
    convergents = compute_convergents(coeffs)

    print(f"\nconvergents are : {convergents}\n")

    for con in convergents:
        tmp_k, tmp_d = con[0], con[1]

        if tmp_k == 0:
            continue

        probable_phi = (e * tmp_d - 1) // tmp_k

        # φ(n) = (p-1)(q-1) = pq - p - q + 1 = n - p - n/p + 1 -->
        # p^2 + p(φ(n) - n - 1) + n = 0
        # if above expression has roots p1, p2 --> c/a = n --> multiplication of two root --> n = p1p2 --> n = p.q
        coefficient_of_equation = [1, probable_phi - N - 1, N]
        answers = np.roots(coefficient_of_equation)
        if len(answers) == 2:
            if np.iscomplex(answers[0]) or np.iscomplex(answers[1]):
                continue
            p, q = round(answers[0]), round(answers[1])
            if p * q == N:
                print("attack was successful")
                print(f"acceptable convergent is {con}")
                print(f"guessed p : {p}, guessed q : {q}")
                return
    print("couldn't break the encryption")


Wiener_attack()
