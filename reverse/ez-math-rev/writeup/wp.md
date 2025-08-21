# ezmath

算法是魔改tea算法，其实关键还是怎么去理解分析这个虚拟机

完全是用位运算实现的虚拟机，这些运算都在堆中实现

举一个例子来分析数据

![image-20250602224011264](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602224011264.png)

这里就是堆中的heap[5000]~heap[5031]这32个字节赋值0或1，heap[5031]是高位，heap[5031]是低位

这里就相当于把heap[5000]~heap[5031]都置1了，这就是全1寄存器，heap[5040]~heap[5071]是全0寄存器

再分析数据读取于存放的代码，其实10个32位值存到了和heap[8000]的位置，最后取数据也是从heap[8000]取出来的



对每一个32位的计算过程来对heap[8000]处的数据分析其变化即可知道每一个过程做了什么

举例：

这里就是将heap[8000]的前8字节数据读取复制到2040和2080

![image-20250602225858542](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602225858542.png)

这一部分实际上实现的就是加法

![image-20250602233002295](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602233002295.png)

左移右移是用or逻辑实现的，如这里就是左移，与全0寄存器的或运算来实现

![image-20250602234126807](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602234126807.png)

再分析其实能发现delta_reg在heap[4000]处

![image-20250602233620834](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602233620834.png)

00010010001101000101011001111000

![image-20250602233603125](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602233603125.png)

分析连续赋值3*4字节的，发现key是在heap[3000]的位置，可取到

key = [0x12345678, 0x9abcdef0, 0x12345678, 0x9abcdef0]



exp

```
#include <stdint.h>
#include <stdio.h>

#define DELTA 0x12345678
#define ROUNDS 32
void tea_decrypt(uint32_t *v, uint32_t *key) {
    uint32_t v0 = v[0], v1 = v[1], sum = DELTA * ROUNDS;
    for (int i = 0; i < ROUNDS; i++) {
        v1 -= ((v0 << 4) + key[2]) ^ (v0 + sum) ^ ((v0 >> 5) + key[3]);
        v0 -= ((v1 << 4) + key[0]) ^ (v1 + sum) ^ ((v1 >> 5) + key[1]);
        sum -= DELTA;
    }
    v[0] = v0;
    v[1] = v1;
}
int main() {
    uint32_t key[4] = {0x12345678, 0x9abcdef0, 0x12345678, 0x9abcdef0};
    uint32_t data1[10] = { 0x2f899590 ,0x90c06101
            ,0x358a1ace ,0x1ac88163
            ,0x5372dec9 ,0xe394bd7f
            ,0x6f3c38aa ,0x4934dddb
            ,0xed39a48e ,0x699afa89};
    // Decrypt all data blocks
    for (int i = 0; i < 10; i += 2) {
        tea_decrypt(&data1[i], key);
    }

    printf("\nDecrypted data:\n");
    for (int i = 0; i < 10; i += 2) {
        printf("%08x %08x\n", data1[i], data1[i + 1]);
    }

    return 0;
}
```

![image-20250602234730365](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602234730365.png)







