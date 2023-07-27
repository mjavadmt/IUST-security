"""
this attack is under chosen cipher text attack which is described as follows:
therefore we're trying to manipulate c(ciphertext) to see what m is.
https://www.tutorialspoint.com/what-are-the-security-of-rsa#:~:text=Factorisation%20attack%20%E2%88%92%20The%20entire%20security,discover%20out%20the%20private%20key.
"""

from sympy import randprime
from random import randint
from math import gcd


def calculate_eulerian(num):
    """
        number of elements in `Reduced Set of Residues` of `num` which doesn't have common divisor with `num`
    """
    if num == 1:
        return 1
    else:
        n = [i for i in range(1, num) if gcd(num, i) == 1]
        return len(n)


def generate_large_prime_number(low, high):
    return randprime(low, high)


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


def create_plain_text(n):
    """
        generate some random plain text to be sent 0 <= m < n
    """
    return randint(0, n)


def create_cipher_text(plain_text, pub_key, n):
    """
        c = m^e mod n
    """
    return (plain_text ** pub_key) % n


def extract_plain_from_cipher(cipher, private_key, n):
    """
        m = c^d mod n
    """
    return (cipher ** private_key) % n


def guess_plain_text(cipher, pub_key, n):
    """
        m ^ e - c = k x n
    """
    m_range = range(0, n)
    guessed_m = 0
    for i in m_range:
        if ((i ** pub_key) - cipher) % n == 0:
            guessed_m = i
            break
    return guessed_m


def guess_private_key(cipher, plain, n, phi):
    """
        in this brute force attack : cipher is known and we extracted plain text by previous function
        on brute forcing each possible plain,
        so if we do following brute force operation we can guess what d is:
        c ^ d = m mod(n)
    """
    possible_d_keys = []
    d_range = range(0, phi)
    for i in d_range:
        if (cipher ** i) % n == plain:
            possible_d_keys.append(i)
    return possible_d_keys


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

    m = create_plain_text(N)  # plain text
    print(f"plain text : {m}")

    print("please wait while calculating cipher text ...")
    c = create_cipher_text(m, e, N)  # cipher text
    print(f"cipher text : {c}")

    print("please wait while calculating deciphered text ...")
    deciphered = extract_plain_from_cipher(c, d, N)  # decrypting the encrypted text
    print(f"decipher text : {deciphered}")

    print()
    if m == deciphered:
        print("***** deciphered is equal to plain text *****")
    else:
        print("***** something gotta go wrong with deciphering operation *****")

    print()

    print("trying to find plain text based on cipher text and brute forcing on any possible plain text ...")
    guessed_plain = guess_plain_text(c, e, N)  # brute force on m until m, meets the conditions.
    print(f"guessed plain text is {guessed_plain}")

    print()

    if guessed_plain == m:
        print("***** guessed plain is equal to plain text *****")
    else:
        print("***** something gotta go wrong with brute forcing on plain text operation *****")

    print()

    print("after finding plain text now we can extract private by brute forcing on each possible value of d")
    guessed_private = guess_private_key(c, m, N, phi_N)
    print(f"correct private key is {d}")
    print(f"possible private keys are {guessed_private}")

    print()
