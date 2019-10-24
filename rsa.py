import random
import math
from time import time

textFileName = "text.txt"
encodedFileName = "encoded.txt"
decodedFileName = "decoded.txt"
privateKeyFileName = "private_key.txt"
publicKeyFileName = "public_key.txt"

primeKeySize = 1024
primeTestIterations = 30
e = 65537

n = 0
d = 0

def binPowMod(num, pow, mod):
    ans = 1
    while pow:
        if pow & 1:
            ans = ans * num % mod
        pow >>= 1
        num = num * num % mod
    return ans

def testMilllerRabin(num):
    if not num % 2:
        return True
    if num == 1:
        return False
    t = num - 1
    s = 0
    while t % 2 == 0:
        t = t // 2
        s += 1
    for _ in range(primeTestIterations):
        a = random.randint(2, num - 2)
        x = binPowMod(a, t, num)
        if x == 1 or x == num - 1:
            continue
        breaked = False
        for __ in range(s - 1):
            x = binPowMod(x, 2, num)
            if x == 1:
                return True
            if x == num - 1:
                breaked = True
                break
        if not breaked:
            return True
    return False

def testSoloveiShtrass(num):
    for i in range(primeTestIterations):
        a = random.randint(2, num - 2)
        if (math.gcd(a, num) > 1):
            return True
        if (binPowMod(a, (num - 1) // 2, num) - JacobySymbol(a, num) % num != 0):
            return True
        return False

def JacobySymbol(a, b):
        if (math.gcd(a, b) != 1):
            return 0
        r = 1
        if (a < 0):
            a = -a
            if (b % 4 == 3):
                r = -r
        while True:
            t = 0
            while (a % 2 == 0):
                t += 1
                a = a / 2

            if not t % 2 == 0:
                if (b % 8 == 3 or b % 8 == 5):
                    r = -r

            if (a % 4) == 3 and b % 4 == 3:
                r = -r

            c = a
            a = b % c
            b = c

            if (a == 0):
                break

        return r

def testTrialDivision(num):
    for i in range(2, int(math.sqrt(num))):
        if num % i == 0:
            return True
    return False

def testWilson(n):
    if (fac(n-1)+1) % n!=0:
        return True
    else:
        return False

def fac(n):
    fac = 1
    i = 0
    while i < n:
        i += 1
        fac = fac * i
    return fac

def generatePrimeNumber():
    num = random.getrandbits(primeKeySize)
    while testSoloveiShtrass(num):
        num = random.getrandbits(primeKeySize)
    return num

def calculateN(p, q):
    return p * q

def calculateFi_n(p, q):
    return (p - 1) * (q - 1)

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    d, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y

def calculateD(fi_n, e):
    return egcd(fi_n, e)[0]

def generateKeys():
    print("Generating keys")
    global n
    global d
    p = generatePrimeNumber()
    q = generatePrimeNumber()
    n = calculateN(p, q)
    fi_n = calculateFi_n(p, q)
    d = egcd(e, fi_n)[1]
    d = (d % fi_n + fi_n) % fi_n

def encode(m, e, n):
    return binPowMod(m, e, n)

def encodeFile(inputFileName, outputFileName, e, n):
    print("Encoding")
    inputFile = open(inputFileName)
    c = list(inputFile.read())
    c = [str(encode(ord(i), e, n)) for i in c]
    outFile = open(outputFileName, "w")
    outFile.write(" ".join(c))

def decode(c, d, n):
    return binPowMod(c, d, n)

def decodeFile(inputFileName, outputFileName, d, n):
    print("Decoding")
    inputFile = open(inputFileName)
    m = inputFile.read().split()
    m = [chr(decode(int(i), d, n)) for i in m]
    outFile = open(outputFileName, "w")
    outFile.write("".join(m))

def saveKey(fileName, a):
    file = open(fileName, "w")
    file.write(str(a))

def loadKey(fileName):
    file = open(fileName)
    return int(file.read())

start = time()
generateKeys()
print(time() - start)
start = time()
encodeFile(textFileName, encodedFileName, e, n)
print(time() - start)
saveKey(publicKeyFileName, n)
saveKey(privateKeyFileName, d)


n = loadKey(publicKeyFileName)
d = loadKey(privateKeyFileName)
start = time()
decodeFile(encodedFileName, decodedFileName, d, n)
print(time() - start)
