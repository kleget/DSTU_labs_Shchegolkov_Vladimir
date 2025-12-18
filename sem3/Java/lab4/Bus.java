package lab4;

public final class Bus extends Car {
    private static final String REGEX = "[ABEKMHOPCTYX]\\s\\d{3}\\s[ABEKMHOPCTYX]{2}\\s\\d{2,3}\\sRUS";

    public Bus(String brand, String color, Engine engine, String registrationNumber) {
        super(brand, CarType.BUS, color, engine, 6, registrationNumber);
    }

    public Bus(String brand, String color, Engine engine) {
        this(brand, color, engine, null);
    }

    @Override
    protected String registrationPattern() {
        return REGEX;
    }

    @Override
    public String toString() {
        return "Bus{" + baseInfo() + "}";
    }
}
