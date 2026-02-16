#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <string.h>

#define SHM_NAME "/collatz_shm"
#define SHM_SIZE 4096

int main(int argc, char *argv[]) {
	if (argc != 2){
		fprintf(stderr, "Usage: %s <starting_number>\n", argv[0]);
		return 1;
	}
	
	int n =  atoi(argv[1]);
	if (n <= 0){
		fprintf(stderr, "Starting number must be positive.\n");
		return 1;
	}

	// Create shared memory object
	int shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
	if (shm_fd == -1) {
		perror("shm_open");
		return 1;
	}

	// Set size of shared memory
	ftruncate(shm_fd, SHM_SIZE);

	// Map shared memory
	char* shm_ptr = mmap(0, SHM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
	if (shm_ptr == MAP_FAILED) {
		perror("mmap");
		return 1;
	}
	pid_t pid = fork();

	// Child process
	if (pid == 0) {
		char buffer[64];
		shm_ptr[0] = '\0';

		while (1) {
			sprintf(buffer, "%d\n", n);
			strcat(shm_ptr, buffer);

			if (n == 1) {
				break;
			} else if (n % 2 == 0) {
				n /= 2;
			} else {
				n = 3 * n + 1;
			}
		}
		munmap(shm_ptr, SHM_SIZE);
		close(shm_fd);
		exit(0);
	}
	// Parent process
	else {
		wait(NULL);

		printf("Collatz sequence:\n%s", shm_ptr);

		// Cleanup
		munmap(shm_ptr, SHM_SIZE);
		close(shm_fd);
		shm_unlink(SHM_NAME);
	}
	return 0;
}



