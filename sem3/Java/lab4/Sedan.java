package lab4;

public class Sedan extends Car {
    private static final String REGEX = "[ABEKMHOPCTYX]\\s\\d{3}\\s[ABEKMHOPCTYX]{2}\\s\\d{2,3}\\sRUS";

    public Sedan(String brand, String color, Engine engine, String registrationNumber) {
        super(brand, CarType.SEDAN, color, engine, 4, registrationNumber);
    }

    public Sedan(String brand, String color, Engine engine) {
        this(brand, color, engine, null);
    }

    @Override
    protected String registrationPattern() {
        return REGEX;
    }

    @Override
    public String toString() {
        return "Sedan{" + baseInfo() + "}";
    }
}
