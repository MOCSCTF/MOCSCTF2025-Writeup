# Content

windows驱动基础

最近学习windows内核，如下题目是driver程序，逆向也可以分析出来，但是目的是为了让大家学习driver入门；

vm启动按F8

![image-20250325124952277](./image-20250325124952277.png)

禁用签名；

![image-20250325125005183](./image-20250325125005183.png)

涉及软件Dbgview和kdm的使用；


## 5-xxoorr

4个考点：驱动加载，xor还原文件；此题目涉及R0-R3通信，是题目3的小进阶；题目4是r0进行解密，此题目为r3解密

```c
MOCSCTF{R0_3_C0m_JuNkC0d3_You_Get!!}
```

查看文件属性

![image-20250324171932077](./image-20250324171932077.png)

运行看看

![image-20250324171955105](./image-20250324171955105.png)

既然提示了找windows的驱动文件，看下资源；

![image-20250324172100995](./image-20250324172100995.png)

看下两个资源，41和42，因为驱动文件都是PE文件，PE头是4D5A，显然数据被加密了；文件名称为xxoorr，这也是个提示；

![image-20250324172248802](./image-20250324172248802.png)

尝试异或找到两个文件的key是0xcc和0xaa；使用010还原文件；

![image-20250324172353627](./image-20250324172353627.png)

![image-20250324172418345](./image-20250324172418345.png)

看到了

![image-20250324172455952](./image-20250324172455952.png)

![image-20250324172506075](./image-20250324172506075.png)

可以按第3题目进行逆向或驱动加载获取flag；与第3题目的加密key不同；找到加密key；

![image-20250324172859932](./image-20250324172859932.png)

![image-20250324172939184](./image-20250324172939184.png)

以后获取flag;

```c
#include <stdio.h>
#include <string.h>

void xor_string(char *str, const char *key, int key_len) {
    int str_len = strlen(str);
    for (int i = 0; i < str_len; i++) {
        str[i] ^= key[i % key_len]; // 循环使用密钥
    }
}

int main() {
    char key[] = {0x38, 0x34, 0x32, 0x30}; 
    char flag[] = {0x75,0x7b,0x71,0x63,0x7b,0x60,0x74,0x4b,0x6a,0x4,0x6d,0x3,0x67,0x77,0x2,0x5d,0x67,0x7e,0x47,0x7e,0x53,0x77,0x2,0x54,0xb,0x6b,0x6b,0x5f,0x4d,0x6b,0x75,0x55,0x4c,0x15,0x13,0x4d}; // 密钥数组
    int key_len = sizeof(key); // 计算密钥数组的长度

    // 异或操作
    xor_string(flag, key, key_len);

    // 输出异或后的结果
        printf("Flag:%s\n", flag);

    return 0;
}
```

![image-20250324173022915](./image-20250324173022915.png)
