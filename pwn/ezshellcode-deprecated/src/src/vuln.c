#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void vuln(char *name, int index)
{
  char buf[1095] =   "Let's see if it works!?!!";
  printf("Old buffer: %s\n", buf);
  char *ptr = buf + index;
  printf("Pointer address: %p\n", ptr);
  strcpy(ptr, name);
  printf("New buffer: %s\n", buf);
  printf("Fresh data: %s\n", ptr);
}

int main(int argc, char *argv[])
{
  if (argc < 3) { 
    printf("Please enter new data and offset");
    return 1;
  }
  vuln(argv[1], atoi(argv[2]));
  printf("Returned to main\n");
  return 0;
}



