#include <err.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <assert.h>
#include <openssl/evp.h>

#include "brek.h"

#define BLOCK_SIZE 16
#define PAGE_SIZE 4096

void hexdump(const char *x, int len) {
    for (int i = 0; i < len; i += 16) {
        printf("%08x:", i);
        for (int j = i; j < len && j < i+16; j+=2) {
            printf(" %02x%02x", x[j] & 0xFF, x[j+1] & 0xFF);
        }
        printf("\n");
    }
}

void decrypt(char *plaintext, char *ciphertext, char *key) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    if (!EVP_CipherInit(ctx, EVP_aes_128_cfb(), key, key, 0)) errx(1, "eci");
    EVP_CIPHER_CTX_set_padding(ctx, 0);

    int len = 0;
    if (!EVP_CipherUpdate(ctx, plaintext, &len, ciphertext, BLOCK_SIZE)) errx(1, "ecu");
    if (len != BLOCK_SIZE) errx(1, "bs");

    EVP_CIPHER_CTX_free(ctx);
}


int main(int argc, const char **argv) {
    alarm(100);

    char *flag = mmap((void*) 0xf1460000, PAGE_SIZE, PROT_READ, MAP_PRIVATE, open("FLAG", 0), 0);
    if (flag == MAP_FAILED) err(1, "can't read flag");

    char *payload = mmap((void*) 0xb0070000, PAGE_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANON | MAP_PRIVATE, -1, 0);
    if (payload == MAP_FAILED) err(1, "can't allocate buffer");

    printf("Expecting bootloader (%d bytes)\n", PAGE_SIZE);
    fflush(stdout);

    char buf[4096] = {};
    fread(buf, PAGE_SIZE, 1, stdin);

    char *key = flag;

    for (int i=0; i < PAGE_SIZE; i += BLOCK_SIZE) {
        decrypt(&payload[i], &buf[i], key);
    }


    printf("Booting...\n");
    fflush(stdout);

    alarm(2);

    ((void(*)())payload)();

    printf("Shutting down.\n");
}
