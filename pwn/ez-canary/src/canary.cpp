#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
int backdoor() {
	char shell[] = "/bin/sh"; 
	asm (
		"xor %%rdi, %%rdi;"             
		"xor %%rsi, %%rsi;"             
		"xor %%rdx, %%rdx;"             
		"mov $0x3b, %%rax;"             
		"lea %0, %%rdi;"                 
		"syscall;"                      
		:
			: "m" (shell)                    
			: "%rax", "%rdi", "%rsi", "%rdx" 
			);
	return 0;
}

int init() {
#include <stdio.h>
	
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
	return 0;
}
int main(){
	init();
	char buf[0x20];
	memset(buf, 0, sizeof(buf));
	puts("Let’s have a head-on battle with canary");
	puts("find it and get it");
	read(0,buf,0x10);
	printf("nature's gift:");
	printf(buf);
	puts("start your attack");
	read(0,buf,0x40);
	return 0;
}
