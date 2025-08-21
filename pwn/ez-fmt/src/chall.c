#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char bss_buf[256];


void str_test(){
    puts("Welcome to SU_ezstr");

    while (1) {
        printf("Input your message: ");
        read(0, bss_buf, sizeof(bss_buf) - 1);
        if(strcmp(bss_buf, "su str done!") == 0){
            return ;
        }
        bss_buf[sizeof(bss_buf) - 1] = '\0';
        puts("Message saved.");
        printf("Your message:\n");
        printf(bss_buf);  
        puts("");
    }
}
void shell() {
    system("/bin/sh");
}
int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    str_test();
    

    return 0;
}