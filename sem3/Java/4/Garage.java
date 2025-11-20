// File: lab4/Garage.java
package lab4;

enum CarStatus {
    AT_BASE, IN_MISSION, IN_REPAIR
}

public class Garage {
    private final Car[] cars;
    private final CarStatus[] statuses;
    private int currentSize;

    public Garage(int maxCapacity) {
        this.cars = new Car[maxCapacity];
        this.statuses = new CarStatus[maxCapacity];
        this.currentSize = 0;
    }

    public boolean addCar(Car car) {
        if (currentSize >= cars.length) {
            System.out.println("Гараж полон.");
            return false;
        }
        cars[currentSize] = car;
        statuses[currentSize] = CarStatus.AT_BASE;
        currentSize++;
        System.out.println("Автомобиль добавлен на базу.");
        return true;
    }

    public boolean removeCar(Car car) {
        for (int i = 0; i < currentSize; i++) {
            if (cars[i] == car) {
                // Сдвигаем массив влево
                for (int j = i; j < currentSize - 1; j++) {
                    cars[j] = cars[j + 1];
                    statuses[j] = statuses[j + 1];
                }
                currentSize--;
                System.out.println("Автомобиль списан.");
                return true;
            }
        }
        System.out.println("Автомобиль не найден в гараже.");
        return false;
    }

    public boolean sendToMission(Car car) {
        for (int i = 0; i < currentSize; i++) {
            if (cars[i] == car && statuses[i] == CarStatus.AT_BASE) {
                statuses[i] = CarStatus.IN_MISSION;
                System.out.println("Автомобиль отправлен в рейс.");
                return true;
            }
        }
        System.out.println("Автомобиль не на базе или не найден.");
        return false;
    }

    public boolean sendToRepair(Car car) {
        for (int i = 0; i < currentSize; i++) {
            if (cars[i] == car && statuses[i] == CarStatus.AT_BASE) {
                statuses[i] = CarStatus.IN_REPAIR;
                System.out.println("Автомобиль отправлен в ремонт.");
                return true;
            }
        }
        System.out.println("Автомобиль не на базе или не найден.");
        return false;
    }

    public boolean returnFromMission(Car car) {
        for (int i = 0; i < currentSize; i++) {
            if (cars[i] == car && statuses[i] == CarStatus.IN_MISSION) {
                statuses[i] = CarStatus.AT_BASE;
                System.out.println("Автомобиль возвращен из рейса.");
                return true;
            }
        }
        System.out.println("Автомобиль не в рейсе или не найден.");
        return false;
    }

    public boolean returnFromRepair(Car car) {
        for (int i = 0; i < currentSize; i++) {
            if (cars[i] == car && statuses[i] == CarStatus.IN_REPAIR) {
                statuses[i] = CarStatus.AT_BASE;
                System.out.println("Автомобиль возвращен из ремонта.");
                return true;
            }
        }
        System.out.println("Автомобиль не в ремонте или не найден.");
        return false;
    }

    public void displayCarsAtBase() {
        System.out.println("Автомобили на базе:");
        boolean found = false;
        for (int i = 0; i < currentSize; i++) {
            if (statuses[i] == CarStatus.AT_BASE) {
                System.out.println(" - " + cars[i]);
                found = true;
            }
        }
        if (!found) System.out.println(" Нет.");
    }

    public void displayCarsInMission() {
        System.out.println("Автомобили в рейсе:");
        boolean found = false;
        for (int i = 0; i < currentSize; i++) {
            if (statuses[i] == CarStatus.IN_MISSION) {
                System.out.println(" - " + cars[i]);
                found = true;
            }
        }
        if (!found) System.out.println(" Нет.");
    }

    public void displayCarsInRepair() {
        System.out.println("Автомобили в ремонте:");
        boolean found = false;
        for (int i = 0; i < currentSize; i++) {
            if (statuses[i] == CarStatus.IN_REPAIR) {
                System.out.println(" - " + cars[i]);
                found = true;
            }
        }
        if (!found) System.out.println(" Нет.");
    }
}