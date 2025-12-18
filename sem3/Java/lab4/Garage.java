package lab4;

enum CarStatus {
    AT_BASE,
    IN_MISSION,
    IN_REPAIR
}

public class Garage {
    private final Car[] cars;
    private final CarStatus[] statuses;
    private int currentSize;

    public Garage(int maxCapacity) {
        if (maxCapacity <= 0) {
            throw new IllegalArgumentException("maxCapacity must be positive");
        }
        this.cars = new Car[maxCapacity];
        this.statuses = new CarStatus[maxCapacity];
        this.currentSize = 0;
    }

    public boolean addCar(Car car) {
        if (currentSize >= cars.length) {
            System.out.println("Garage is full.");
            return false;
        }
        cars[currentSize] = car;
        statuses[currentSize] = CarStatus.AT_BASE;
        currentSize++;
        System.out.println("Car added to base.");
        return true;
    }

    public boolean removeCar(Car car) {
        for (int i = 0; i < currentSize; i++) {
            if (cars[i] == car) {
                for (int j = i; j < currentSize - 1; j++) {
                    cars[j] = cars[j + 1];
                    statuses[j] = statuses[j + 1];
                }
                cars[currentSize - 1] = null;
                statuses[currentSize - 1] = null;
                currentSize--;
                System.out.println("Car removed from base.");
                return true;
            }
        }
        System.out.println("Car not found.");
        return false;
    }

    public boolean sendToMission(Car car) {
        return changeStatus(car, CarStatus.AT_BASE, CarStatus.IN_MISSION, "Car sent to mission.");
    }

    public boolean sendToRepair(Car car) {
        return changeStatus(car, CarStatus.AT_BASE, CarStatus.IN_REPAIR, "Car sent to repair.");
    }

    public boolean returnFromMission(Car car) {
        return changeStatus(car, CarStatus.IN_MISSION, CarStatus.AT_BASE, "Car returned from mission.");
    }

    public boolean returnFromRepair(Car car) {
        return changeStatus(car, CarStatus.IN_REPAIR, CarStatus.AT_BASE, "Car returned from repair.");
    }

    private boolean changeStatus(Car car, CarStatus from, CarStatus to, String successMessage) {
        for (int i = 0; i < currentSize; i++) {
            if (cars[i] == car && statuses[i] == from) {
                statuses[i] = to;
                System.out.println(successMessage);
                return true;
            }
        }
        System.out.println("Operation is not allowed in current state or car missing.");
        return false;
    }

    public void displayCarsAtBase() {
        displayByStatus("Cars at base:", CarStatus.AT_BASE);
    }

    public void displayCarsInMission() {
        displayByStatus("Cars in mission:", CarStatus.IN_MISSION);
    }

    public void displayCarsInRepair() {
        displayByStatus("Cars in repair:", CarStatus.IN_REPAIR);
    }

    private void displayByStatus(String title, CarStatus status) {
        System.out.println(title);
        boolean found = false;
        for (int i = 0; i < currentSize; i++) {
            if (statuses[i] == status) {
                System.out.println(" - " + cars[i]);
                found = true;
            }
        }
        if (!found) {
            System.out.println(" (none)");
        }
    }
}
