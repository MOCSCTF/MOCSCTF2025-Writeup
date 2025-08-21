## flag

MOCSCTF{Machin3_Learning_and_Crypto_QAQ}

## 解題步驟

首先需要分析題目所給的源碼，主要是對TPM這個類別的理解，搜尋可以知道這是一個樹形奇偶機，本題是基於它來做金鑰交換的方案。題目基於不同的參數做了兩次金鑰交換，分別得到aes-cbc加密所需的key和iv。因此我們需要透過分析該金鑰交換過程漏洞得到key和iv解密。

其實就是具有一個隱藏層的前向反饋神經網絡，在做密鑰交換的時候，alice和bob的初始權重W不同，但是傳入的x相同，若干次做forward之後，如果兩者得到的結果相等，說明出現了權重相同的情況，那麼把權重作為密鑰即可（密鑰交換成功）。

本題對於iv取得的金鑰交換過程，選取得參數k l n為3，3，3。這樣的話權重W的空間太小了，價值為：$7^{3*3}=7^{9}$，直接爆破就行了。

第二部分的問題在於給了太多密鑰交換的資訊了，給了inputs，alice_taus，bob_taus，利用這些資訊可以透過機率統計的方法隨機猜測權重更新過程，具體的可以參考https://arxiv.org/pdf/0711.2411.pdf#page=33 的攻擊方法，exp如下：

```python
import hashlib
import numpy as np
from Crypto.Cipher import AES
from output import ct, inputs, alice_taus, bob_taus
from itertools import product
from tqdm import tqdm
from binascii import unhexlify

def theta(a, b):
    return 1 if a == b else 0

def decrypt(key, iv, ct):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return cipher.decrypt(unhexlify(ct))
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

# https://arxiv.org/pdf/0711.2411.pdf#page=33
def geometry(TPM: TPM, tau):
    wx = np.sum(TPM.x * TPM.W, axis=1)
    h_i = wx / np.sqrt(TPM.n)
    min_idx = np.argmin(np.abs(h_i))
    nonzero = np.where(TPM.roe == 0, -1, TPM.roe)
    TPM.roe[min_idx] = -nonzero[min_idx]
    TPM.tau = np.sign(np.prod(TPM.roe))

    if TPM.tau == tau:
        TPM.backward(tau)


Eve = TPM(8, 10, 10, "rule1")
for i in range(999):
    if alice_taus[i] == bob_taus[i]:
        if alice_taus[i] == Eve.forward(np.array(inputs[i])):
            Eve.backward(alice_taus[i])
        else:
            geometry(Eve, alice_taus[i])

key = hashlib.sha256(Eve.W.tobytes()).digest()

t = range(-3,3+1)
for i in tqdm(product(t,repeat = 3*3)):
    i = np.array(i).reshape(3, 3)
    sha256 = hashlib.sha256()
    sha256.update(i.tobytes())
    iv = sha256.digest()[:16]
    pt = decrypt(key,iv,ct)
    if b'MOCSCTF' in pt:
        print(pt)
        break
```

