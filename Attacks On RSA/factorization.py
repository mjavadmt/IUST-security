"""
    this kind of attack is considered as factorization attack which has following procedure:
    Factorisation attack − The entire security of RSA depends on the assumption that it is impossible for the attacker
    to factor the number N into two factors P and Q. If the attacker is able to discover out P or Q from the equation
    N = P x Q thus the attacker can discover out the private key.
    this will happen when N is small number which can be easily factored into its prime numbers
    https://www.tutorialspoint.com/what-are-the-security-of-rsa#:~:text=Factorisation%20attack%20%E2%88%92%20The%20entire%20security,discover%20out%20the%20private%20key.
"""

from sympy.ntheory import factorint
from sympy import randprime
from random import randint
from math import gcd


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


def generate_public_key(phi):
    """
        1 < e < phi(n) , gcd(e, phi(n) = 1
    """
    tmp_e = randint(2, phi)
    while gcd(tmp_e, phi) != 1:  # loop until gcd(e, phi(n)) = 1
        tmp_e = randint(2, phi)
    return tmp_e


def generate_private_key(pub_key, phi):
    """
        e.d = 1 mod phi(n) --> d = e^(phi(phi(n)) - 1) mod phi(n)
    """
    return (pub_key ** (calculate_eulerian(phi) - 1)) % phi


def factorize_number(n):
    return factorint(n)


if __name__ == "__main__":

    print()
    low_num = 1e1
    high_num = 5e1

    p = generate_large_prime_number(low_num, high_num)  # generate large prime number between low and high
    q = generate_large_prime_number(low_num, high_num)  # generate large prime number between low and high
    while q == p:  # loop until `q` gets unequal to `p`
        q = generate_large_prime_number(low_num, high_num)

    N = p * q
    phi_N = (p - 1) * (q - 1)

    print(f"p : {p}, q : {q}")
    print(f"n = p x q, n : {N}")
    print(f"φ(n) = (p-1) x (q-1), φ(n) = {phi_N}")

    print(f"{'-' * 50}")

    e = generate_public_key(phi_N)  # public key
    print(f"public key : {e}")

    print("please wait while calculating private key ...")
    d = generate_private_key(e, phi_N)  # private key
    print(f"private key : {d}")

    print(f"{'-' * 50}")

    print("now we try to factorize N which is public to everybody")
    n_factors = factorize_number(N)
    # as we know RSA choosing N based on two prime number so `n_factors` should have 2 number in it
    if len(n_factors) == 2:
        print(f"this is correct version of RSA because factors are : {n_factors}")
    else:
        print(f"this is wrong version because factors are : {n_factors}")

    print()

    print("after extracting factors we can perceive what is φ(n)")
    factors = list(n_factors.keys())
    phi_calculated_by_factors = (factors[0] - 1) * (factors[1] - 1)
    print(f"calculated φ(n) is : {phi_calculated_by_factors}")
    print("comparing φ(n) calculated")
    if phi_calculated_by_factors == phi_N:
        print("main version of φ(n) is equal to derived version of φ(n) after factorization")
    else:
        print("main version of φ(n) is not equal to derived version of φ(n) after factorization")

    private_key_by_eve = generate_private_key(e, phi_calculated_by_factors)

    print(f"private key gained by eve is {private_key_by_eve}")

    if private_key_by_eve == d:
        print("now we have private key of sender and listen to his/her messages")
    else:
        print("the private key acquired from eve is not equal to sender private key")

    print()
