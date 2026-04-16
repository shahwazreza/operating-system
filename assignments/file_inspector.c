#include <stdio.h>
#include <sys/stat.h>
#include <stdlib.h>

void inspect_file(const char* filepath) {
    struct stat file_stat;

    printf("Inspecting: %s\n", filepath);

    // Call stat()
    if (stat(filepath, &file_stat) == -1) {
        perror("Error");
        return;
    }

    // Print file size
    printf("Size: %ld bytes\n", file_stat.st_size);

    // Check file type
    if (S_ISDIR(file_stat.st_mode)) {
        printf("Type: Directory\n");
    } else if (S_ISREG(file_stat.st_mode)) {
        printf("Type: Regular File\n");
    } else {
        printf("Type: Other\n");
    }

    printf("\n");
}

int main() {
    // Create a test file
    FILE *f = fopen("test.txt", "w");
    if (f) {
        fputs("Hello File System!", f);
        fclose(f);
    }

    inspect_file("test.txt");
    inspect_file(".");
    inspect_file("does_not_exist.bin");

    return 0;
}