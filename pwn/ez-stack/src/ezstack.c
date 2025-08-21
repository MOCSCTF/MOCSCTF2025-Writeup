#include"stdio.h"
#include"unistd.h"
#include"stdlib.h"
void init() {
    setvbuf(stdin, NULL, _IONBF, 0); 
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(){
	init();
	char buf[24];
	printf("try to get the flag\n");
	read(0,buf,72);
}

int vuln(){
	char buf[24];
	char s1[24];
	int i=0;
	printf("say something\n");
	read(0,buf,8);
	for(i=0;i<8;i++){
		if(buf[i]=="b"||buf[i]=='i'||buf[i]=="n"||buf[i]=="/"||buf[i]=="s"||buf[i]=="h"){
			printf("it's may not a good choice\n");
			return 0;		
		}
		if(buf[i]="$"||buf[i]=="f"||buf[i]=="l"||buf[i]=="a"||buf[i]=="g"){
			printf("no way\n");
			return 0;
		}
		if(buf[i]>="0"&&buf[i]<="9"){
			return 0;
		}
	}
	system(buf);

}
//gcc -fno-pie -no-pie -fno-stack-protector -o vuln vuln.c  



