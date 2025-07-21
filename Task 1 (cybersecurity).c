#include <stdio.h>
#include <ctype.h>
#include <string.h>

void checkPasswordStrength(char password[]) {
    int length = strlen(password);
    int hasUpper = 0;
    int hasLower = 0;
    int hasDigit = 0;
    int hasSpecial = 0;

    for (int i = 0; i < length; i++) {
        if (isupper(password[i])) {
            hasUpper = 1;
        } else if (islower(password[i])) {
            hasLower = 1;
        } else if (isdigit(password[i])) {
            hasDigit = 1;
        } else {
            hasSpecial = 1;
        }
    }

    int criteria = hasUpper + hasLower + hasDigit + hasSpecial;

    printf("Password Analysis:\n");
    printf("Length: %d\n", length);
    printf("Contains Uppercase: %s\n", hasUpper ? "Yes" : "No");
    printf("Contains Lowercase: %s\n", hasLower ? "Yes" : "No");
    printf("Contains Digit: %s\n", hasDigit ? "Yes" : "No");
    printf("Contains Special Character: %s\n", hasSpecial ? "Yes" : "No");

    if (length < 6 || criteria < 2) {
        printf("Password Strength: WEAK\n");
    } else if (length >= 6 && length < 10 && criteria >= 3) {
        printf("Password Strength: MEDIUM\n");
    } else if (length >= 10 && criteria == 4) {
        printf("Password Strength: STRONG\n");
    } else {
        printf("Password Strength: MEDIUM\n");
    }
}

int main() {
    char password[100];

    printf("Enter your password: ");
    scanf("%99s", password);

    checkPasswordStrength(password);

    return 0;
}
