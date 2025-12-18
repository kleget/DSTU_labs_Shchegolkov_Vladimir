package lab4;

public class SpecialCar extends Car {
    private static final String REGEX = "[A-Z]{2}-\\d{4}";

    public SpecialCar(String brand, String color, Engine engine, String registrationNumber) {
        super(brand, CarType.SPECIAL, color, engine, 4, registrationNumber);
    }

    public SpecialCar(String brand, String color, Engine engine) {
        this(brand, color, engine, null);
    }

    @Override
    protected String registrationPattern() {
        return REGEX;
    }

    @Override
    public String toString() {
        return "SpecialCar{" + baseInfo() + "}";
    }
}
