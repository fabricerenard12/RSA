import random
import secrets

#Returns the greatest common divisor of a and b using the euclidean algorithm
def gcd(a: 'int', b: 'int') -> 'gcd(a,b), list of operations':
    if b == 0:
        return a, [[a, 0]]

    operations = []
    rem = a % b
    while rem:
        operations.append([a, b])
        a = b
        b = rem
        rem = a % b
    
    operations.append([a, b])
    operations.append([b, 0])
    return b, operations

#Returns the modular inverse of a modulo n in {1, ..., n - 1} using the extended euclidean algorithm
def modularInverse(a: 'int', n: 'int') -> 'inverse of a modulo n in {1, ..., n - 1}':

    #Computes the Bézout's coefficients to find an inverse of a modulo n
    def compute(operations: 'list'):
        k = len(operations)
        while k:
            if k == len(operations):
                x = 1
                y = 0
                k -= 1
                continue
            prev_x = x
            prev_y = y
            x = prev_y
            y = prev_x - (operations[k - 1][0] // operations[k - 1][1]) * prev_y
            k -= 1
        return x

    #Returns the inverse of a modulo n in {1, ..., n - 1}
    def adjust(x: 'int'):
        if x > (n - 1):
            x -= n
            return(adjust(x))
        if x < 1:
            x += n
            return(adjust(x))
        return x

    if gcd(a, n)[0] != 1:
        return None
    return adjust(compute(gcd(a, n)[1]))

#Returns the result of a base raised to a certain power modulo n using binary exponentiation
def modularExponentiation(base: 'int', power: 'int', mod: 'int') -> 'base ** power % mod':
    if mod == 1:
        return 0
    res = 1
    base = base % mod
    while power > 0:
        if power % 2 == 1:
            res = (res * base) % mod
        base = (base * base) % mod
        power = power // 2
    return res

#Returns the jacobi symbol of a and p
def jacobi(a: 'int', p: 'int') -> '0, 1 or -1':
    a = int(a)
    p = int(p)
    if gcd(a, p)[0] != 1:
        return 0

    if a > p:
        return jacobi(a % p, p)
    
    if a % 2 == 0:
        m = int(-1) ** int((((p ** 2) - 1) // 8))
        return m * jacobi(a // 2, p)

    if a == 1:
        return 1
        
    m = int(-1) ** int(((a - 1) * (p - 1)) // 4)
    return m * jacobi(p, a)

#Returns whether an integer n is prime or not using the Solovay-Strassen primality test
def solovayStrassen(n: 'int', k: 'int' = 40) -> 'bool':
    if k == 0 or n == 2:
        return True
    a = random.randrange(2, n)
    m = modularExponentiation(a, int((n - 1) // 2), n)
    if jacobi(a, n) == 0 or jacobi(a, n) % n != m:
        return False
    return solovayStrassen(n, k - 1)

#Returns an n bits prime number
def generatePrime(n: 'int, bits', k: 'int' = 40) -> 'Probably prime number':
    a = secrets.randbits(n)
    if solovayStrassen(a, k):
        return a
    return generatePrime(n, k)

#Returns the value of phi(n)
def euler(p: 'int', q: 'int') -> 'phi(n)':
    return (p - 1) * (q - 1)

#Encrypts a message using RSA encryption   
def encryptionRSA(p: 'int', q: 'int', message: 'int', encryptionKey: 'int' = None) -> 'info string':
    def key():
        e = secrets.randbelow(euler(p, q))
        if gcd(e, euler(p, q))[0] != 1:
            return key()
        return e

    n = p * q
    if gcd(message, n)[0] != 1:
        raise ValueError('Message and n have to be coprime integers')
    if message >= n:
        raise ValueError('Message has to be strictly inferior than n.')

    if encryptionKey == None:
        encryptionKey = key()
    decryptionKey = modularInverse(encryptionKey, euler(p, q))
    encryptedMessage = modularExponentiation(message, encryptionKey, n)
    
    return f'Public keys: n: {n} and e: {encryptionKey}, Private keys: p: {p}. q: {q} and d: {decryptionKey}, Encrypted message: {encryptedMessage}'

#Decrypts a message using RSA decryption 
def decryptionRSA(p: 'int', q: 'int', decryptionKey: 'int', encryptedMessage: 'int') -> 'info string':
    n = p * q
    encryptionKey = modularInverse(decryptionKey, euler(p, q))
    decryptedMessage = modularExponentiation(encryptedMessage, decryptionKey, n)
    return f'Public keys: n: {n} and e: {encryptionKey}, Private keys: p: {p}. q: {q} and d: {decryptionKey}, Decrypted message: {decryptedMessage}'


