#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *chinese_table[] = {
    "氢", "氦", "锂", "铍", "硼", "碳", "氮", "氧", "氟", "氖", "钠",
    "镁", "铝", "硅", "磷", "硫", "氯", "氩", "钾", "钙", "钪", "钛",
    "钒", "铬", "锰", "铁", "钴", "镍", "铜", "锌", "镓", "锗", "砷",
    "硒", "溴", "氪", "铷", "锶", "钇", "锆", "铌", "钼", "锝", "钌",
    "铑", "钯", "银", "镉", "铟", "锡", "锑", "碲", "碘", "氙", "铯",
    "钡", "镧", "铈", "镨", "钕", "钷", "钐", "铕", "钆"};
const char *padding_char = "金";

const char *key = "Mitsuha";
const char *expected_result = "锝钆镨钌镨氙钯钡铕硼铟碘钪锆砷锌砷铁硒镍钐氯硼"
                              "铑铍镉钛镁氙氮氦硫铷铟金金";


void rc4(unsigned char *data, int data_len, const char *key,
         unsigned char *output) {
  unsigned char S[256];
  int key_len = strlen(key);
  int i, j = 0, k, t;

  for (i = 0; i < 256; ++i)
    S[i] = i;
  for (i = 0; i < 256; ++i) {
    j = (j + S[i] + (unsigned char)key[i % key_len]) % 256;
    unsigned char tmp = S[i];
    S[i] = S[j];
    S[j] = tmp;
  }

  i = j = 0;
  for (int idx = 0; idx < data_len; ++idx) {
    i = (i + 1) % 256;
    j = (j + S[i]) % 256;
    unsigned char tmp = S[i];
    S[i] = S[j];
    S[j] = tmp;
    k = S[(S[i] + S[j]) % 256];
    output[idx] = data[idx] ^ k;
  }
}

void base64_custom_encode(unsigned char *data, int len, char *output) {
  int i, j;
  int pad = 0;
  char buffer[1024] = {0}; 
  buffer[0] = '\0';

  for (i = 0; i < len; i += 3) {
    int chunk[3] = {0};
    int bytes = len - i >= 3 ? 3 : len - i;

    for (j = 0; j < bytes; ++j)
      chunk[j] = data[i + j];

    if (bytes < 3)
      pad = 3 - bytes;

    int n = (chunk[0] << 16) | (chunk[1] << 8) | chunk[2];

    int indices[4] = {(n >> 18) & 0x3F, (n >> 12) & 0x3F, (n >> 6) & 0x3F,
                      n & 0x3F};

    for (j = 0; j < 4 - pad; ++j)
      strcat(buffer, chinese_table[indices[j]]);
    for (j = 0; j < pad; ++j)
      strcat(buffer, padding_char);
  }

  strcpy(output, buffer);
}

int main() {

  char input[256];
  printf("Please input your flag: ");
  fgets(input, sizeof(input), stdin);

  size_t len = strlen(input);
  if (input[len - 1] == '\n')
    input[len - 1] = '\0';

  unsigned char encrypted[512];
  memset(encrypted, 0, sizeof(encrypted));
  rc4((unsigned char *)input, strlen(input), key, encrypted);

  char encoded_result[2048];
  memset(encoded_result, 0, sizeof(encoded_result));
  base64_custom_encode(encrypted, strlen(input), encoded_result);

  printf("After encrypt: %s\n", encoded_result);

  if (strcmp(encoded_result, expected_result) == 0) {
    printf("Success! The flag is correct.\n");
  } else {
    printf("Failed! Incorrect flag.\n");
  }

  return 0;
}
