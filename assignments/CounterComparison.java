import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.atomic.AtomicInteger;

public class CounterComparison {

    interface Counter {
        void increment();

        int getCount();
    }

    static class LockCounter implements Counter {
        private int count = 0;
        private ReentrantLock lock = new ReentrantLock();

        public void increment() {
            lock.lock();
            try {
                count++;
            } finally {
                lock.unlock();
            }
        }

        public int getCount() {
            return count;
        }
    }

    static class AtomicCounter implements Counter {
        private AtomicInteger count = new AtomicInteger(0);

        public void increment() {
            count.incrementAndGet();
        }

        public int getCount() {
            return count.get();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        testCounter(new LockCounter(), "LockCounter");
        testCounter(new AtomicCounter(), "AtomicCounter");
    }

    private static void testCounter(Counter counter, String name) throws InterruptedException {

        Thread[] threads = new Thread[4];
        long start = System.nanoTime();

        for (int i = 0; i < 4; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 100000; j++) {
                    counter.increment();
                }
            });
            threads[i].start();
        }

        for (Thread t : threads)
            t.join();

        long end = System.nanoTime();

        System.out.println(name + " Final Count: " + counter.getCount());
        System.out.println(name + " Time: " + (end - start) + " ns\n");
    }
}
