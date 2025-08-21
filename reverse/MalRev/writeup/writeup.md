## MalRev

题目涉及来源于最近常见且猖獗的恶意黑产软件，黑猫、银狐、钓鱼等；此类恶意软件设计思路为白+黑方式，即在已有软件的基础上将黑文件掺入，达到C2控制目的。

## 解题思路

### 运行查看

运行程序查看，依次出现如下弹窗 can you find the flag? 说明dll被劫持了；

![==image-20250615230035085==](img//image-20250615230035085.png)

查看程序为x64，将exe文件拖入IDA，看导入表；程序自定义的导入dll如下；

![image-20250615222654388](img//image-20250615222654388.png)

### 依次查看dll获取key

#### clipboard_watcher_plugin.dll

导出表

![image-20250615232019670](img//image-20250615232019670.png)

查看函数，典型的白加黑测试；

![image-20250615232043029](img//image-20250615232043029.png)

返回看主函数

![image-20250615232103185](img//image-20250615232103185.png)

跟进

![image-20250615232118847](img//image-20250615232118847.png)

跟进，clipboard_watcher_plugin，第一个弹窗在这里；

![image-20250615232134948](img//image-20250615232134948.png)

发现算法和数据

![image-20250615232213408](img//image-20250615232213408.png)

进行异或的值

![image-20250615232233710](img//image-20250615232233710.png)

异或结果

```c
{0xB9, 0xF9, 0xB9, 0x6A, 0xA4}
```

依次跟进剩余dll

#### desktop_multi_window_plugin.dll

![image-20250615232457025](img//image-20250615232457025.png)

![image-20250615232510238](img//image-20250615232510238.png)

![image-20250615232520482](img//image-20250615232520482.png)

异或结果

```c
{0x9F, 0xF8, 0xD9, 0x25, 0x0C}

```

#### flutter_webrtc_plugin.dll

![image-20250615232702859](img//image-20250615232702859.png)

![image-20250615232716548](img//image-20250615232716548.png)

![image-20250615232726069](img//image-20250615232726069.png)

异或结果

```c
{0x92, 0xF7, 0xD4, 0x2E, 0x09}

```

#### screen_retriever_plugin.dll

![image-20250615232807340](img//image-20250615232807340.png)

![image-20250615232817191](img//image-20250615232817191.png)

![image-20250615232823735](img//image-20250615232823735.png)

异或结果

```c
{0xBA, 0xDF, 0xDC, 0x20, 0x09}

```

#### window_manager_plugin.dll

![image-20250615232844765](img//image-20250615232844765.png)

![image-20250615232854665](img//image-20250615232854665.png)

![image-20250615232902547](img//image-20250615232902547.png)

异或结果

```c
{0xEA, 0xDF, 0xBC, 0x20, 0x59}
```

题目中有个encrypt文件，猜测是用key进行解密；这里就是异或，不过异或key是上述连接；

```c
0xB9,0xF9,0xB9,0x6A,0xA4,0x9F,0xF8,0xD9,0x25,0x0C,0x92,0xF7,0xD4,0x2E,0x09,0xBA,0xDF,0xDC,0x20,0x09,0xEA,0xDF,0xBC,0x20,0x59
```

### XOR解密encrypt文件

![image-20250615233221391](img//image-20250615233221391.png)

解密后查看文件发现是exe文件

![image-20250615233248613](img//image-20250615233248613.png)

执行或拖入IDA拿到flag

![image-20250615233358506](img//image-20250615233358506.png)

```c
MOCSCTF{4829a5a29aebf281a7e1ba5e94a2e0bb}
```



