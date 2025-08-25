## flag

MOCSCTF{0767cb48c145213beb976f00d7f843e5}

## 解題步驟

1. volatility 掃描進程，發現記事本。

![image-20250615092313711](img/image-20250615092313711.png)

![image-20250615092350040](img/image-20250615092350040.png)


2. 查看記事本，發現正在編輯hosts 文件，文件中找到flag。

![image-20250615092428767](img/image-20250615092428767.png)

flag：MOCSCTF{0767cb48c145213beb976f00d7f843e5}