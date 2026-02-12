import java.util.concurrent.Semaphore;
import java.util.Random;

public class ParkingGarageSimulation {

    static class ParkingGarage {
        private Semaphore semaphore;
        private int carsInside = 0;

        public ParkingGarage(int capacity) {
            semaphore = new Semaphore(capacity);
        }

        public void park(String carName) {
            try {
                System.out.println(carName + " is trying to enter...");

                semaphore.acquire();

                synchronized (this) {
                    carsInside++;
                    System.out.println(carName + " has entered. Slots used: " + carsInside);
                }

                Thread.sleep(new Random().nextInt(2000) + 1000);

                synchronized (this) {
                    carsInside--;
                    System.out.println(carName + " left. Slots freed.");
                }

                semaphore.release();

            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {

        ParkingGarage garage = new ParkingGarage(3);

        for (int i = 1; i <= 10; i++) {
            String carName = "Car-" + i;
            new Thread(() -> garage.park(carName)).start();
        }
    }
}
