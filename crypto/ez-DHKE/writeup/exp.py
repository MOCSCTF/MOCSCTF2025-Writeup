import hashlib
import numpy as np
from Crypto.Cipher import AES
from output import ct, inputs, alice_taus, bob_taus
from itertools import product
from tqdm import tqdm
from binascii import unhexlify

def theta(a, b):
    return int(a == b)

def decrypt(key, iv, ct):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return cipher.decrypt(unhexlify(ct))

class TPM:
    def __init__(self, k=3, n=4, l=6, rule="rule1"):
        self.k, self.n, self.l = k, n, l
        self.W = np.random.randint(-l, l + 1, (k, n))
        self.rule = rule

    def forward(self, x):
        self.x = x.reshape(self.W.shape)
        self.roe = np.sign(np.sum(self.W * self.x, axis=1))
        self.tau = np.prod(self.roe)
        return self.tau

    def update(self, tau):
        for (i, j), _ in np.ndenumerate(self.W):
            if self.rule == "rule1":
                delta = self.x[i, j] * self.roe[i] * theta(self.tau, tau) * theta(self.roe[i], self.tau)
            else:
                delta = self.x[i, j] * theta(self.tau, tau) * theta(self.roe[i], self.tau)
            self.W[i, j] = np.clip(self.W[i, j] + delta, -self.l, self.l)

def geometry(tpm, tau):
    wx = np.sum(tpm.x * tpm.W, axis=1)
    h_i = wx / np.sqrt(tpm.n)
    min_idx = np.argmin(np.abs(h_i))
    tpm.roe[min_idx] = -1 if tpm.roe[min_idx] == 0 else -tpm.roe[min_idx]
    tpm.tau = np.sign(np.prod(tpm.roe))
    if tpm.tau == tau:
        tpm.update(tau)

Eve = TPM(8, 10, 10, "rule1")

for i in range(999):
    if alice_taus[i] == bob_taus[i]:
        if alice_taus[i] == Eve.forward(np.array(inputs[i])):
            Eve.update(alice_taus[i])
        else:
            geometry(Eve, alice_taus[i])

Eve.W=np.array(Eve.W, dtype=np.int32)
key = hashlib.sha256(Eve.W.tobytes()).digest()
print("Eve's key:", key.hex())
t = range(-3, 4)
for i in tqdm(product(t, repeat=9)):
    iv = hashlib.sha256(np.array(i,dtype=np.int32).reshape(3, 3).tobytes()).digest()[:16]
    pt = decrypt(key, iv, ct)
    if b'MOCSCTF' in pt:
        print("flag:",pt)
        break

