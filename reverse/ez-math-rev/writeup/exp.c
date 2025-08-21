#include <stdint.h>
#include <stdio.h>

#define DELTA 0x12345678
#define ROUNDS 32
void tea_decrypt(uint32_t *v, uint32_t *key) {
    uint32_t v0 = v[0], v1 = v[1], sum = DELTA * ROUNDS;
    for (int i = 0; i < ROUNDS; i++) {
        v1 -= ((v0 << 4) + key[2]) ^ (v0 + sum) ^ ((v0 >> 5) + key[3]);
        v0 -= ((v1 << 4) + key[0]) ^ (v1 + sum) ^ ((v1 >> 5) + key[1]);
        sum -= DELTA;
    }
    v[0] = v0;
    v[1] = v1;
}
int main() {
    uint32_t key[4] = {0x12345678, 0x9abcdef0, 0x12345678, 0x9abcdef0};
    uint32_t data1[10] = { 0x2f899590 ,0x90c06101
            ,0x358a1ace ,0x1ac88163
            ,0x5372dec9 ,0xe394bd7f
            ,0x6f3c38aa ,0x4934dddb
            ,0xed39a48e ,0x699afa89};
    // Decrypt all data blocks
    for (int i = 0; i < 10; i += 2) {
        tea_decrypt(&data1[i], key);
    }

    printf("\nDecrypted data:\n");
    for (int i = 0; i < 10; i += 2) {
        printf("%08x %08x\n", data1[i], data1[i + 1]);
    }

    return 0;
}
