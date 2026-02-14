import java.util.Scanner;

class MatrixWorker extends Thread {
    private int row;
    private int[][] A, B, C;
    private int colsA, colsB;

    public MatrixWorker(int row, int[][] A, int[][] B, int[][] C, int colsA, int colsB) {
        this.row = row;
        this.A = A;
        this.B = B;
        this.C = C;
        this.colsA = colsA;
        this.colsB = colsB;
    }

    public void run() {
        for (int j = 0; j < colsB; j++) {
            C[row][j] = 0;
            for (int k = 0; k < colsA; k++) {
                C[row][j] += A[row][k] * B[k][j];
            }
        }
    }
}

public class MatrixThreads {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        // User inputs Matrix A
        System.out.print("Enter rows of Matrix A: ");
        int rowsA = input.nextInt();

        System.out.print("Enter columns of Matrix A: ");
        int colsA = input.nextInt();

        int[][] A = new int[rowsA][colsA];

        System.out.println("Enter elements of Matrix A:");
        for (int i = 0; i < rowsA; i++) {
            for (int j = 0; j < colsA; j++) {
                A[i][j] = input.nextInt();
            }
        }

        // User inputs Matrix B
        System.out.print("Enter rows of Matrix B: ");
        int rowsB = input.nextInt();

        System.out.print("Enter columns of Matrix B: ");
        int colsB = input.nextInt();

        if (colsA != rowsB) {
            System.out.println("Matrix multiplication not possible.");
            return;
        }

        int[][] B = new int[rowsB][colsB];

        System.out.println("Enter elements of Matrix B:");
        for (int i = 0; i < rowsB; i++) {
            for (int j = 0; j < colsB; j++) {
                B[i][j] = input.nextInt();
            }
        }

        int[][] C = new int[rowsA][colsB];
        MatrixWorker[] threads = new MatrixWorker[rowsA];

        // Seperate worker thread to compute each row
        for (int i = 0; i < rowsA; i++) {
            threads[i] = new MatrixWorker(i, A, B, C, colsA, colsB);
            threads[i].start();
        }

        try {
            for (int i = 0; i < rowsA; i++) {
                threads[i].join();
            }
        } catch (InterruptedException e) {
            System.out.println("Thread interrupted.");
        }

        // Output
        System.out.println("Result Matrix C:");
        for (int i = 0; i < rowsA; i++) {
            for (int j = 0; j < colsB; j++) {
                System.out.printf("%5d", C[i][j]);
            }
            System.out.println();
        }

        input.close();
    }
}
