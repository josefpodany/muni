#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "md5.h"

const char transformationTable[8][12][3] = {
    {"a", "@4"}, {"b", "8"}, {"e", "3"}, {"i", "!"}, {"l", "1"}, {"o", "0"}, {"s", "$5"}, {"t", "7"},
};

int charIsTransformable(char plaintextChar, const char transformationTable[8][12][3]) {
    for (int i = 0; i < 8; i++)
        if (plaintextChar == transformationTable[i][0][0] || plaintextChar + 32 == transformationTable[i][0][0])
            return strlen(transformationTable[i][1]);
    return 0;
}

int getPasswdMultiTransMask(char *plaintext, char *multicharMask, const char transformationTable[8][12][3]) {
    int plaintextSize = strlen(plaintext);
    int multicharMaskValue = 0;
    for (int i = 0; i < plaintextSize; i++) {
        if (charIsTransformable(plaintext[i], transformationTable) == 2) {
            multicharMaskValue = (multicharMaskValue << 1) + 1;
            multicharMask[i] = '1';
        } else
            multicharMask[i] = '0';
    }
    multicharMask[plaintextSize] = '\0';
    return multicharMaskValue;
}

int getPasswdTransMask(char *plaintext, char *stringMask, const char transformationTable[8][12][3]) {
    // Create binary representation of possible transformation combinations.
    int plaintextSize = strlen(plaintext);
    int maskValue = 0;
    for (int i = 0; i < plaintextSize; i++) {
        if (charIsTransformable(plaintext[i], transformationTable)) {
            maskValue = (maskValue << 1) + 1;
            stringMask[i] = '1';
        } else {
            stringMask[i] = '0';
        }
    }
    stringMask[plaintextSize] = '\0';
    return maskValue;
}

void createHash(MD5_CTX *md5Ctx, char *plaintext, char *hashAsString) {
    int plaintextSize = strlen(plaintext);
    unsigned char hash[16];
    MD5_Init(md5Ctx);
    MD5_Update(md5Ctx, plaintext, plaintextSize);
    MD5_Final(hash, md5Ctx);
    for (int i = 0; i < 16; i++)  // convert hash from hexa to string format
        sprintf(&hashAsString[i * 2], "%02x", (unsigned int)hash[i]);
}

int getTransformedChar(char c, const char transformationTable[8][12][3], int charPos) {
    for (int i = 0; i < 8; i++) {
        if (c == transformationTable[i][0][0] || c + 32 == transformationTable[i][0][0]) {
            return transformationTable[i][1][charPos];
        }
    }
    return '-';
}

void transformString(char *plaintext, char *modifiedPlaintext, char *stringMask, int shiftedMask, int substPos) {
    int plaintextSize = strlen(plaintext);
    for (int cPos = plaintextSize - 1; cPos >= 0 && shiftedMask != 0; cPos--) {
        if (stringMask[cPos] == '1' && (shiftedMask & 1) != 0) {
            modifiedPlaintext[cPos] = getTransformedChar(plaintext[cPos], transformationTable, substPos);
            shiftedMask = shiftedMask >> 1;
        } else if (stringMask[cPos] == '1' && (shiftedMask & 1) == 0) {
            shiftedMask = shiftedMask >> 1;
        }
    }
}

int generateHashAndCompare(char *plaintext, char *targetHash, const char transformationTable[8][12][3],
                           bool transformations) {
    MD5_CTX md5Ctx;
    int plaintextSize = strlen(plaintext);
    char hashAsString[33];
    createHash(&md5Ctx, plaintext, hashAsString);
    if (!strcmp(hashAsString, targetHash)) return 0;
    if (!transformations) return 1;

    char stringMask[plaintextSize];
    char multiTransMask[plaintextSize];
    int maskValue = getPasswdTransMask(plaintext, stringMask, transformationTable);
    int multiTransMaskValue = getPasswdMultiTransMask(plaintext, multiTransMask, transformationTable);
    for (int i = 1; i <= maskValue; i++) {
        char modifiedPlaintext[strlen(plaintext)];
        strcpy(modifiedPlaintext, plaintext);  // store string of modified plaintext with applied transformations
        int shiftedMask = i;
        // substitute characters
        transformString(plaintext, modifiedPlaintext, stringMask, shiftedMask, 0);
        createHash(&md5Ctx, modifiedPlaintext, hashAsString);
        if (!strcmp(hashAsString, targetHash)) {
            strcpy(plaintext, modifiedPlaintext);
            return 0;
        }
        char multiTransPlaintext[plaintextSize];
        strcpy(multiTransPlaintext, modifiedPlaintext);
        // second round of substitution for chars, that have 2 options to transform to
        for (int j = 1; j <= multiTransMaskValue; j++) {
            strcpy(multiTransPlaintext, modifiedPlaintext);
            int shiftedMultiMask = j;
            transformString(plaintext, multiTransPlaintext, multiTransMask, shiftedMultiMask, 1);
            createHash(&md5Ctx, multiTransPlaintext, hashAsString);
            if (!strcmp(hashAsString, targetHash)) {
                strcpy(plaintext, multiTransPlaintext);
                return 0;
            }
        }
    }
    return 1;
}

void readLine(char *plaintext, FILE *file) {
    int i = 0, tmp = 0;
    memset(plaintext, '\0', 33);
    while (tmp != '\n' && tmp != EOF) {
        tmp = fgetc(file);
        plaintext[i] = tmp;
        i++;
    }
    plaintext[i - 1] = '\0';
}

int main(int argc, char **argv) {
    const int maxPassSize = 37;  // hardcoded -> looked up max size of passwd in provided dict
    char plaintext[maxPassSize + 1];
    bool transformation = false;
    FILE *dictionary = NULL;
    char comparedHash[33];

    if (argc == 4) {
        if (strcmp(argv[1], "-t")) {
            fprintf(stderr, "ERROR: Received unrecognized flag '%s'\n", argv[1]);
            return 1;
        }
        if (strlen(argv[3]) != 32) {
            fprintf(stderr, "ERROR: Provided hash does not have excatly size of 32\n");
            return 1;
        }
        transformation = true;
        dictionary = fopen(argv[2], "r");
        strcpy(comparedHash, argv[3]);
    } else if (argc == 3) {
        if (strlen(argv[2]) != 32) {
            fprintf(stderr, "ERROR: Provided hash does not have excatly size of 32\n");
            return 1;
        }
        dictionary = fopen(argv[1], "r");
        strcpy(comparedHash, argv[2]);
    } else {
        fprintf(stderr, "ERROR: Received wrong number of arguments\n");
        return 1;
    }
    if (dictionary == NULL) {
        fprintf(stderr, "ERROR: Could not open provided file with plain-text passwords\n");
        return 1;
    }

    while (!feof(dictionary)) {
        readLine(plaintext, dictionary);
        if (!generateHashAndCompare(plaintext, comparedHash, transformationTable, transformation)) {
            printf("password found\n%s\n", plaintext);
            fclose(dictionary);
            return 0;
        }
    }

    printf("password not found\n");
    fclose(dictionary);
    return 0;
}