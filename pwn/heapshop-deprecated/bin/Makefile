.POSIX:

CFLAGS = -g -no-pie -s -m64 -Wl,-z,relro,-z,now 

heapshop: heapshop.c
	$(CC) $(CFLAGS) -o heapshop heapshop.c