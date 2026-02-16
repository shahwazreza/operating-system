// Assignment 1 Reza Shahwaz

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <sys/types.h>

#define BUFFER_SIZE 100

int main(){
    int fd[2];
    pid_t pid;
    char buffer[BUFFER_SIZE];

    // Credit to chatgpt for showing me the use of pipe and fork system calls

    // Create a pipe
    if (pipe(fd) == -1) {
        perror("pipe");
        return 1;
    }

    // Fork a child process
    pid = fork();

    if (pid < 0) {
        perror("fork");
        return 1;
    }

    // Parent process
    if (pid > 0) {
        close(fd[0]); // Close unused read end

        printf("Enter a string: ");
        fgets(buffer, BUFFER_SIZE, stdin);

        // Write the string to the pipe
        write(fd[1], buffer, strlen(buffer) + 1);
        close(fd[1]); // Close write end after writing
    }
    // Child process
    else {
        close(fd[1]); // Close unused write end

        // Read the string from the pipe
        read(fd[0], buffer, BUFFER_SIZE);

        // Invert the case 
        for (int i = 0; buffer[i] != '\0'; i++) {
            if (islower(buffer[i])) {
                buffer[i] = toupper(buffer[i]);
            } else if (isupper(buffer[i])) {
                buffer[i] = tolower(buffer[i]);
            }
        }
        // Print
        printf("Modified string: %s", buffer);
        close(fd[0]); // Close read end after reading
    }
    return 0;
}
