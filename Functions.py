import random
from math import gcd as bltin_gcd

# this file contains any backend function(s) for the main file's use


# this is the inverse function between two numbers
def inverse(b, n):
    if n < b:
        temp = n
        n = b
        b = temp
    # p_i and p_j are initialized to 0 and 1 respectively
    # in this instance p_i is p_0 and p_j is p_1
    p = 0
    newp = 1
    a = n
    r = 1
    # the loop will continue to run until the remainder is <= 0 much like EA
    while r > 0:
        # the quotient of a and b is calculated and stored
        q = int(a / b)
        # the remainder of a / b is calculated and stored
        r = int(a % b)
        # the next iteration of p is calculated and stored
        tempP = int((p - (newp * q)) % n)
        # p_i and p_j are reassigned to the next iteration using calculated values
        p = newp
        newp = tempP
        # much like EA, a is swapped with b and b is swapped with the remainder
        a = b
        b = r
        # if the remainder is 1 p_j is returned as the inverse
        if b == 1:
            return newp
    # if the remainder is not 1 and the loop exits and a > 1, there is no inverse
    if a > 1:
        return None


# this function generates a list of prime integers found within a specified range
def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)

    return prime_list


# this function, given a specified number and in this case is a prime number,
# will generate a list of all the primitive roots of that prime
def primRoots(modulo):
    required_set = {num for num in range(1, modulo) if bltin_gcd(num, modulo)}
    return [g for g in range(1, modulo) if required_set == {pow(g, powers, modulo)
                                                            for powers in range(1, modulo)}]


# this function implements the Elgamal encryption algorithm
# parameters include a prime number, the generator alpha, a public key, and the plaintext attempting to be sent
def elgamal_encrypt(prime, alpha, pub_key, plain):
    # for every unique message a random value of k is generated
    k = random.randint(2, 10)
    # the shared key is calculated using the public key, random integer k, and the prime number
    K = pow(pub_key, k) % prime
    # the first half of the ciphertext is calculated using alpha, k, and the prime number
    c1 = pow(alpha, k) % prime
    nums = []
    # the desired message is converted to ALL lowercase
    plain = plain.lower()
    # for any letter a-z converting that letter to ascii then subtracting 96 will allow the letter to fall into the
    # usual 1-26 range when translating from letters to numbers
    # since spaces don't apply to the rule above any space is set as a 0
    for i in plain:
        if i == " ":
            nums.append(0)
        # if the message contains a number that number is make negative and appended
        elif i.isdigit():
            nums.append(int(i)-100)
        else:
            temp = ord(i) - 96
            nums.append(temp)
    c2 = []
    # the second half is calculated using the shared ket K,
    # each translated letter of the plaintext, and the prime number
    for j in nums:
        # does not apply the formula to negative numbers
        if j < 0:
            c2.append(j)
            continue
        temp = K * j % prime
        c2.append(temp)
    cipher = [c1, c2]
    return cipher


# this function implements the Elgamal decryption algorithm
# parameters include a prime number, the ciphertext, and a private key
def elgamal_decrypt(prime, cipher, pr_key):
    # the shared key is calculated using the first half of the ciphertext, the private key,
    # and the prime number
    K = pow(cipher[0], pr_key) % prime
    # if there is no inverse between the shared key and the prime number the function returns NONE
    if inverse(K, prime) is None:
        return None
    # this variable hold the value of the inverse between the shared key and the prime number
    temp = inverse(K, prime)
    letters = []
    plain = ""
    for i in cipher[1]:
        # if the number is a zero which represents a space, simply a zero is appended to the plaintext code
        if i == 0:
            letters.append(0)
            continue
        # checks for negatives that indicate a number in string form
        elif i < 0:
            letters.append(i)
            continue
        else:
            # these line translate the encrypted number back to the proper ascii number
            num = (i * temp % prime) + 96
            letters.append(num)
    for j in letters:
        # if the decryption number is a zero, a space is added to the plaintext
        if j == 0:
            plain += " "
        elif j < 0:
            # makes the negative positive so the string number remains the same
            plain += str(j + 100)
        else:
            # converts the decryption number, ascii number, to an ascii character
            plain += chr(j)
    return plain
