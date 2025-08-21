import numpy as np
from Crypto.Cipher import AES
import hashlib
from Crypto.Util.Padding import pad

flag = b'MOCSCTF{Machin3_Learning_and_Crypto_QAQ}'

theta = lambda a,b: 1 if a == b else 0

def encrypt(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return cipher.encrypt(pad(plaintext, 16)).hex()

class TPM:
    def __init__(self, k=3, n=4, l=6, rule="rule1"):

        self.k = k
        self.n = n
        self.l = l
        self.W = np.random.randint(-l, l + 1, (k, n))
        self.rule = rule

    def forward(self, x):

        self.x = x.reshape(self.W.shape)
        self.roe = np.sign(np.sum(self.W * self.x, axis=1))
        self.tau = np.prod(self.roe)
        return self.tau

    def hebian(self, tau):
        for (i, j), _ in np.ndenumerate(self.W):
            self.W[i, j] += self.x[i, j] * self.roe[i] * theta(self.tau, tau) * theta(self.roe[i], self.tau)
            self.W[i, j] = np.clip(self.W[i, j], -self.l, self.l)

    def random_walk(self, tau):
        for (i, j), _ in np.ndenumerate(self.W):
            self.W[i, j] += self.x[i, j] * theta(self.tau, tau) * theta(self.roe[i], self.tau)
            self.W[i, j] = np.clip(self.W[i, j], -self.l, self.l)
    def backward(self, tau):
        if self.rule == "rule1":
            self.hebian(tau)
        elif self.rule == "rule2":
            self.random_walk(tau)


k, l, n = 8, 10, 10
Alice = TPM(k, n, l, "rule1")
Bob = TPM(k, n, l, "rule1")

inputs = []
alice_taus = []
bob_taus = []

for _ in range(999):
    x = np.random.randint(-27, 28, Alice.n * Alice.k)
    t1 = Alice.forward(x)
    t2 = Bob.forward(x)
    inputs.append(list(x))
    alice_taus.append(t1)
    bob_taus.append(t2)
    if t1 == t2:
        Alice.backward(Bob.tau)
        Bob.backward(Alice.tau)

assert np.array_equal(Bob.W, Alice.W)
assert Bob.W.shape == (k, n)
sha256 = hashlib.sha256()
sha256.update(Alice.W.tobytes())
key = sha256.digest()

# another one
k,l,n = 3, 3, 3
Alice = TPM(k, n, l, "rule2")
Bob = TPM(k, n, l, "rule2")

for _ in range(888):
    x = np.random.randint(-25, 26, Alice.n * Alice.k)
    t1 = Alice.forward(x)
    t2 = Bob.forward(x)
    if t1 == t2:
        Alice.backward(Bob.tau)
        Bob.backward(Alice.tau)

assert np.array_equal(Bob.W, Alice.W)
assert Bob.W.shape == (k, n)
sha256 = hashlib.sha256()
sha256.update(Alice.W.tobytes())
iv = sha256.digest()
ct = encrypt(key, iv[:16], flag)
with open("output.py", "w") as f:
    f.write(f"ct = {ct}\n")
    f.write(f"inputs = {inputs}\n")
    f.write(f"alice_taus = {alice_taus}\n")
    f.write(f"bob_taus = {bob_taus}\n")