public class RaceConditionBank {

    static class BankAccount {
        private int balance = 1000;

        // Delete Keyword synchronized for part A
        // Add Keyword synchronized for Part B
        public synchronized void updateBalance(int amount) {
            int currentBalance = balance;

            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            currentBalance += amount;
            balance = currentBalance;
        }

        public int getBalance() {
            return balance;
        }
    }

    public static void main(String[] args) throws InterruptedException {

        BankAccount account = new BankAccount();
        Thread[] threads = new Thread[10];

        // 5 deposits
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> account.updateBalance(100));
        }

        // 5 withdrawals
        for (int i = 5; i < 10; i++) {
            threads[i] = new Thread(() -> account.updateBalance(-100));
        }

        for (Thread t : threads)
            t.start();
        for (Thread t : threads)
            t.join();

        System.out.println("Final Balance: " + account.getBalance());
    }
}
