#include "kernel/types.h"
#include "user/user.h"

#define N 1000

int main() {
    int pipe1[2], pipe2[2];
    char byte = 'x';
    int i;

    if(pipe(pipe1) < 0 || pipe(pipe2) < 0) {
        fprintf(2, "Pipe failed\n");
        exit(1);
    }

    int pid = fork();
    if(pid < 0) exit(1);

    int start = (int)uptime();

    if(pid == 0){
        for(i = 0; i < N; i++){
            if(read(pipe1[0], &byte, 1) != 1) exit(1);
            if(write(pipe2[1], &byte, 1) != 1) exit(1);
        }
        exit(0);
    } else {
        for(i = 0; i < N; i++){
            if(write(pipe1[1], &byte, 1) != 1) exit(1);
            if(read(pipe2[0], &byte, 1) != 1) exit(1);
        }

        int end = (int)uptime();
        int elapsed = end - start;

        printf("Exchanges: %d, Time ticks: %d\n", N, elapsed);
        printf("Exchanges per tick: %d\n", N / elapsed);

        wait(0);
    }

    exit(0);

