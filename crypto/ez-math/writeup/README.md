## flag

MOCSCTF{M4th_1s_fUn_RDY}

## 解題步驟

本題的解決分為三個主要步驟：首先根據給定的 n 和 p,q 的差值 delta 分解 n；然後處理公鑰指數 e 與歐拉函數 ϕ(n) 不互素的情況；最後進行模 n 開平方根求解原始訊息。

### 步驟 0: 根據 **n** 和 **delta** 分解得到 **p** 和 **q**!

1. 建立關係:

 已知 n=p⋅q 且 q−p=delta。 

 由第二個式子可得 q=p+delta。

2. 代入消元:

 將 q=p+delta 代入 n=p⋅q：

 n=p(p+delta)⟹n=p2+p⋅delta

3. 構造一元二次方程式:

 整理上式，得到一個關於 p 的一元二次方程式：

 p2+delta⋅p−n=0

4. 求解方程式:

 使用一元二次方程式的求根公式 p=2−delta±delta2+4n。 

由於 p 必須是正素數，我們取正根：p=2−delta+delta2+4n。 

令 D=delta2+4n。計算 s=D。 

則 p=(s−delta)/2 和 q=(s+delta)/2。

### 步驟 1: 處理 **e** 與 **ϕ(n)** 不互素

1. 計算 ϕ(n):

 ϕ(n)=(p−1)(q−1)。

2. 計算 g=gcd(e,ϕ(n)):

 題目設計使得 g=2。

3. 計算 c′≡mg(modn):

 目標是找出 c′≡mg(modn)。 

令 eg=e/g 和 ϕg=ϕ(n)/g。 

計算 d0≡(eg)−1(modϕg)。 

然後計算 c′≡cd0(modn)。此時 c′≡mg(modn)。由於 g=2, 即 c′≡m2(modn)。

### 步驟 2: 模 **n** 開 **g** 次根 (即模 **n** 開平方)

現在的問題是求解 m2≡c′(modn)。

1. **分別解模** p **和模** q **的平方根：**

 - 解 xp2≡c′(modp) 使用 Tonelli-Shanks 演算法 (例如 `sympy.ntheory.residue_ntheory.sqrt_mod`)。得到解 ±rp。 
- 解 xq2≡c′(modq) 使用 Tonelli-Shanks 演算法。得到解 ±rq。 
- Tonelli-Shanks 演算法的理論基礎與費馬小定理相關，例如判斷二次剩餘時所使用的勒讓德符號 a(p−1)/2(modp)。

2. 使用中國剩餘定理 (CRT) 合併解：

 我們有四組同餘方程組，每一組都會給出一個模 n 的唯一解 m：

 (±rp(modp),±rq(modq))

3. 確定正確的 m：

 將得到的4個候選 m 值嘗試轉換為位元組串，符合 MOCSCTF{...} 格式的就是flag。
