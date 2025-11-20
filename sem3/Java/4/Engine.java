// File: lab4/Engine.java
package lab4;

public class Engine {
    private final String serialNumber;
    private final double power;
    private final double displacement;
    private final double fuelConsumption;
    private final String fuelType;
    private final int cylinders;

    public Engine(String serialNumber, double power, double displacement, double fuelConsumption, String fuelType, int cylinders) {
        this.serialNumber = serialNumber;
        this.power = power;
        this.displacement = displacement;
        this.fuelConsumption = fuelConsumption;
        this.fuelType = fuelType;
        this.cylinders = cylinders;
    }

    // Геттеры
    public String getSerialNumber() { return serialNumber; }
    public double getPower() { return power; }
    public double getDisplacement() { return displacement; }
    public double getFuelConsumption() { return fuelConsumption; }
    public String getFuelType() { return fuelType; }
    public int getCylinders() { return cylinders; }

    @Override
    public String toString() {
        return String.format(
            "Engine{serialNumber='%s', power=%.2f, displacement=%.2f, fuelConsumption=%.2f, fuelType='%s', cylinders=%d}",
            serialNumber, power, displacement, fuelConsumption, fuelType, cylinders
        );
    }
}