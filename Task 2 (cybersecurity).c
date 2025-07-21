#include <stdio.h>
#include <ctype.h>

void encrypt(char* message, int shift) {
    for (int i = 0; message[i] != '\0'; i++) {
        char ch = message[i];
        if (isalpha(ch)) {
            char base = isupper(ch) ? 'A' : 'a';
            message[i] = (ch - base + shift) % 26 + base;
        }
    }
}

void decrypt(char* message, int shift) {
    encrypt(message, 26 - (shift % 26));  // Reverse shift
}

int main() {
    char message[1000];
    int shift;

    printf("Enter the message: ");
    fgets(message, sizeof(message), stdin);  // Reads full line

    printf("Enter the shift value: ");
    scanf("%d", &shift);

    encrypt(message, shift);
    printf("\nEncrypted message: %s", message);

    decrypt(message, shift);
    printf("Decrypted message: %s", message);

    return 0;
}