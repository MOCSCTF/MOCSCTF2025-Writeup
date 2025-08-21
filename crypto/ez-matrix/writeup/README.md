## flag

MOCSCTF{Easy_chall3nge_of_matr1x_trace}

## 解題步驟

題目把flag轉成二進位位元（01序列），然後對於0和1分別使用不同的矩陣產生函數來加密成矩陣。

scrambled_matrix_0先生成了數值在2-7的矩陣A，然後得到了A的相似矩陣$B=P*A*P^{-1}$

而scrambled_matrix_1則是產生了模65537下的隨機矩陣。

### 部署sage
1. 建立容器
```
docker run -p8888:8888 sagemath/sagemath:latest sage-jupyter
```
2. 導入sage library
```
pip install pycryptodome
pip install tqdm
```
3. 編輯寫入並使用 Sage 控制台打開，輸入“shift+enter”以執行命令
```
vim exp.py
from sage.all import *
```
4. 將exp.py 的內容貼到命令提示字元上