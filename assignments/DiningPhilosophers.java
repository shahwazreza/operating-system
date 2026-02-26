import java.util.concurrent.Semaphore;
import java.util.concurrent.locks.ReentrantLock;

public class DiningPhilosophers {

    static final int NUM_PHILOSOPHERS = 5;
    static final int THINK_TIME = 1000;
    static final int EAT_TIME = 2000;

    static long startTime = System.currentTimeMillis();

    static String timestamp() {
        long elapsed = (System.currentTimeMillis() - startTime) / 1000;
        long min = elapsed / 60;
        long sec = elapsed % 60;
        return String.format("[%02d:%02d]", min, sec);
    }

    static synchronized void log(String msg) {
        System.out.println(timestamp() + " " + msg);
    }

    static class Fork {
        int id;
        ReentrantLock lock = new ReentrantLock();

        Fork(int id) {
            this.id = id;
        }
    }

    static class Philosopher extends Thread {
        int id;
        Fork left;
        Fork right;
        Semaphore butler;

        Philosopher(int id, Fork left, Fork right, Semaphore butler) {
            this.id = id;
            this.left = left;
            this.right = right;
            this.butler = butler;
        }

        void think() throws InterruptedException {
            log("Philosopher " + id + " is Thinking.");
            Thread.sleep(THINK_TIME);
        }

        void eat() throws InterruptedException {
            log("Philosopher " + id + " is Eating.");
            Thread.sleep(EAT_TIME);
        }

        public void run() {
            try {
                while (true) {
                    think();

                    butler.acquire();

                    Fork first = (left.id < right.id) ? left : right;
                    Fork second = (left.id < right.id) ? right : left;

                    first.lock.lock();
                    if (first == left)
                        log("Philosopher " + id + " picked up Left Fork.");
                    else
                        log("Philosopher " + id + " picked up Right Fork.");

                    second.lock.lock();
                    if (second == right)
                        log("Philosopher " + id + " picked up Right Fork.");
                    else
                        log("Philosopher " + id + " picked up Left Fork.");

                    eat();

                    second.lock.unlock();
                    if (second == right)
                        log("Philosopher " + id + " put down Right Fork.");
                    else
                        log("Philosopher " + id + " put down Left Fork.");

                    first.lock.unlock();
                    if (first == left)
                        log("Philosopher " + id + " put down Left Fork.");
                    else
                        log("Philosopher " + id + " put down Right Fork.");

                    butler.release();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Fork[] forks = new Fork[NUM_PHILOSOPHERS];
        for (int i = 0; i < NUM_PHILOSOPHERS; i++)
            forks[i] = new Fork(i);

        Semaphore butler = new Semaphore(NUM_PHILOSOPHERS - 1);

        Philosopher[] philosophers = new Philosopher[NUM_PHILOSOPHERS];

        for (int i = 0; i < NUM_PHILOSOPHERS; i++) {
            Fork left = forks[i];
            Fork right = forks[(i + 1) % NUM_PHILOSOPHERS];
            philosophers[i] = new Philosopher(i + 1, left, right, butler);
            philosophers[i].start();
        }

        // There was no clear indication of how long the program should run in the
        // assignment description.
        // To avoid an infinite loop, I am suspending the program after 30 seconds
        Thread.sleep(30000);
        System.exit(0);
    }
}