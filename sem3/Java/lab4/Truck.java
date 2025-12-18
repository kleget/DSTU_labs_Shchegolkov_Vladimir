package lab4;

public class Truck extends Car {
    private static final String REGEX = "[ABEKMHOPCTYX]\\s\\d{3}\\s[ABEKMHOPCTYX]{2}\\s\\d{2,3}\\sRUS";

    public Truck(String brand, String color, Engine engine, String registrationNumber) {
        super(brand, CarType.TRUCK, color, engine, 6, registrationNumber);
    }

    public Truck(String brand, String color, Engine engine) {
        this(brand, color, engine, null);
    }

    @Override
    protected String registrationPattern() {
        return REGEX;
    }

    @Override
    public String toString() {
        return "Truck{" + baseInfo() + "}";
    }
}
