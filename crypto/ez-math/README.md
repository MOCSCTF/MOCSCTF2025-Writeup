## 題目名稱：ez_math

## 題目類型：crypto

## 題目難度：3星

## 題目說明：

1. 挑戰概述

本 RSA 挑戰包含四個部分。參賽者需要利用不同 RSA 密碼體制的特性或漏洞來解出每一部分的密文，得到一個整數。將該整數通過 `long_to_bytes()` 函數（例如 Python 的 `Crypto.Util.number.long_to_bytes`）轉換，即可得到一部分 FLAG。集齊所有部分，拼接成完整的 FLAG。

**總 FLAG 格式**: `MOCSCTF{part1_part2_part3_part4}` (實際 FLAG 是 `MOCSCTF{y0U_AR3_a_gO0d_learN3er}`)

**FLAG 分段**:

- 第一部分: `MOCSCTF{`
- 第二部分: `y0U_AR3_`
- 第三部分: `a_gO0d_l`
- 第四部分: `earN3er}`

2. 各部分設計及參數