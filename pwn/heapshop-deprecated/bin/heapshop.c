#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 1

void alloc();
void delete();
void show();
void bye();
int promptIdx();

char* arr[SIZE];

int main(void)
{
  int choice;
  int ops;

  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  puts("Welcome to the Heap Shop!");

  ops = 0;
  while(1) {
    if(ops >= 15) {
      puts("Too many operations. Exiting...");
      bye();
    }
    ops++;

    puts("===== Menu =====");
    puts("1. Allocate item");
    puts("2. Delete item");
    puts("3. Show item");
    puts("4. Exit");
    printf("Select an option: ");
    scanf("%d", &choice);

    switch(choice) {
      case 1: 
        alloc();
        break;
      case 2:
        delete();
        break;
      case 3: 
        show();
        break;
      case 4:
        bye();
    }
  }
}

int promptIdx() {
  int idx;

  printf("Enter item index (0-%d): ", SIZE - 1);
  scanf("%d", &idx);

  if(idx < 0 || idx >= SIZE) bye();

  return idx;
}

void alloc() {
  int idx;
  int size;
  int amt;

  puts("== Allocate Item ==");
  idx = promptIdx();

  printf("Enter size (max 4096): ");
  scanf("%d", &size);
  getchar();

  if(size <= 0 || size > 0x1000) bye();

  arr[idx] = (char*) malloc(size);

  printf("Enter item data: ");
  amt = read(0, arr[idx], size - 1);

  if(amt == -1) bye();
  arr[amt] = '\x00';
}

void delete() {
  int idx;

  puts("== Delete Item ==");
  idx = promptIdx();

  free(arr[idx]);

  puts("Item deleted.");
}

void show() {
  int idx;

  puts("== Show Item ==");
  idx = promptIdx();

  puts(arr[idx]);

  puts("End of item.");
}

void bye() {
  puts("Goodbye!");
  _exit(0);
}
