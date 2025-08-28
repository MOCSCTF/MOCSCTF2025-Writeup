## flag

MOCSCTF{4829a5a29aebf281a7e1ba5e94a2e0bb}

## 解題步驟


1. 運行查看

執行程式查看，依序出現如下彈跳視窗 can you find the flag? 說明dll被劫持了；

![image-20250615230035085](img/image-20250615230035085.png)

檢視程式為x64，將exe檔拖曳到IDA，看導入表；程式自訂的導入dll如下；

![image-20250615222654388](img/image-20250615222654388.png)

2. 依序查看dll獲取key

- clipboard_watcher_plugin.dll

匯出表

![image-20250615232019670](img/image-20250615232019670.png)

查看函數，典型的白加黑測試；

![image-20250615232043029](img/image-20250615232043029.png)

返回看主函數

![image-20250615232103185](img/image-20250615232103185.png)

跟進

![image-20250615232118847](img/image-20250615232118847.png)

跟進，clipboard_watcher_plugin，第一個彈跳窗在這裡；

![image-20250615232134948](img/image-20250615232134948.png)

發現演算法和數據

![image-20250615232213408](img/image-20250615232213408.png)

進行異或的值

![image-20250615232233710](img/image-20250615232233710.png)

異或結果

```c
{0xB9, 0xF9, 0xB9, 0x6A, 0xA4}
```

依序跟進剩餘dll

- desktop_multi_window_plugin.dll

![image-20250615232457025](img/image-20250615232457025.png)

![image-20250615232510238](img/image-20250615232510238.png)

![image-20250615232520482](img/image-20250615232520482.png)

異或結果

```c
{0x9F, 0xF8, 0xD9, 0x25, 0x0C}

```

- flutter_webrtc_plugin.dll

![image-20250615232702859](img/image-20250615232702859.png)

![image-20250615232716548](img/image-20250615232716548.png)

![image-20250615232726069](img/image-20250615232726069.png)

異或結果

```c
{0x92, 0xF7, 0xD4, 0x2E, 0x09}

```

- screen_retriever_plugin.dll

![image-20250615232807340](img/image-20250615232807340.png)

![image-20250615232817191](img/image-20250615232817191.png)

![image-20250615232823735](img/image-20250615232823735.png)

異或結果

```c
{0xBA, 0xDF, 0xDC, 0x20, 0x09}

```

- window_manager_plugin.dll

![image-20250615232844765](img/image-20250615232844765.png)

![image-20250615232854665](img/image-20250615232854665.png)

![image-20250615232902547](img/image-20250615232902547.png)

異或結果

```c
{0xEA, 0xDF, 0xBC, 0x20, 0x59}
```

題目中有個encrypt文件，猜測是用key進行解密；這裡就是異或，不過異或key是上述連接；

```c
0xB9,0xF9,0xB9,0x6A,0xA4,0x9F,0xF8,0xD9,0x25,0x0C,0x92,0xF7,0x D4,0x2E,0x09,0xBA,0xDF,0xDC,0x20,0x09,0xEA,0xDF,0xBC,0x20,0x59
```

3. XOR解密encrypt文件

![image-20250615233221391](img/image-20250615233221391.png)

解密後查看文件發現是exe文件

![image-20250615233248613](img/image-20250615233248613.png)

執行或拖入IDA拿到flag

![image-20250615233358506](img/image-20250615233358506.png)

```
MOCSCTF{4829a5a29aebf281a7e1ba5e94a2e0bb}
```



