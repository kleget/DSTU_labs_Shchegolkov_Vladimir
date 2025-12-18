package lab4;

public class Engine {
    private final String serialNumber;
    private final double power;
    private final double displacement;
    private final double fuelConsumption;
    private final String fuelType;
    private final int cylinders;

    public Engine(String serialNumber,
                  double power,
                  double displacement,
                  double fuelConsumption,
                  String fuelType,
                  int cylinders) {
        this.serialNumber = serialNumber;
        this.power = power;
        this.displacement = displacement;
        this.fuelConsumption = fuelConsumption;
        this.fuelType = fuelType;
        this.cylinders = cylinders;
    }

    public String getSerialNumber() {
        return serialNumber;
    }

    public double getPower() {
        return power;
    }

    public double getDisplacement() {
        return displacement;
    }

    public double getFuelConsumption() {
        return fuelConsumption;
    }

    public String getFuelType() {
        return fuelType;
    }

    public int getCylinders() {
        return cylinders;
    }

    @Override
    public String toString() {
        return String.format(
            "Engine{serial='%s', power=%.1f hp, displacement=%.1fL, fuel=%.1f L/100km, type='%s', cylinders=%d}",
            serialNumber,
            power,
            displacement,
            fuelConsumption,
            fuelType,
            cylinders
        );
    }
}
