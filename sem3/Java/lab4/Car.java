package lab4;

import java.util.Objects;
import java.util.regex.Pattern;

/**
 * Base class for cars. Keeps common attributes and enforces registration format checks.
 */
public abstract class Car {
    private final String brand;
    private final CarType type;
    private String color;
    private Engine engine;
    private final int wheelCount;
    private String registrationNumber;

    protected Car(String brand,
                  CarType type,
                  String color,
                  Engine engine,
                  int wheelCount,
                  String registrationNumber) {
        this.brand = Objects.requireNonNull(brand, "brand");
        this.type = Objects.requireNonNull(type, "type");
        this.color = Objects.requireNonNull(color, "color");
        this.engine = Objects.requireNonNull(engine, "engine");
        if (wheelCount <= 0) {
            throw new IllegalArgumentException("wheelCount must be positive");
        }
        this.wheelCount = wheelCount;
        if (registrationNumber != null) {
            setRegistrationNumber(registrationNumber);
        }
    }

    protected Car(String brand, CarType type, String color, Engine engine, int wheelCount) {
        this(brand, type, color, engine, wheelCount, null);
    }

    public final String getBrand() {
        return brand;
    }

    public final CarType getType() {
        return type;
    }

    public String getColor() {
        return color;
    }

    public Engine getEngine() {
        return engine;
    }

    public final int getWheelCount() {
        return wheelCount;
    }

    public String getRegistrationNumber() {
        return registrationNumber;
    }

    public void setColor(String color) {
        this.color = Objects.requireNonNull(color, "color");
    }

    public void setEngine(Engine engine) {
        this.engine = Objects.requireNonNull(engine, "engine");
    }

    /**
     * Sets a registration number if it satisfies the subclass validation rule.
     *
     * @return true when the value is accepted, false otherwise
     */
    public final boolean setRegistrationNumber(String regNumber) {
        Objects.requireNonNull(regNumber, "regNumber");
        if (!Pattern.matches(registrationPattern(), regNumber)) {
            throw new IllegalArgumentException("Invalid registration number format: " + regNumber);
        }
        this.registrationNumber = regNumber;
        return true;
    }

    /**
     * Regular expression that the concrete car type considers valid.
     */
    protected abstract String registrationPattern();

    protected String baseInfo() {
        return String.format(
            "brand='%s', type=%s, color='%s', engine=%s, wheels=%d, reg='%s'",
            brand,
            type,
            color,
            engine,
            wheelCount,
            registrationNumber == null ? "-" : registrationNumber
        );
    }

    @Override
    public String toString() {
        return "Car{" + baseInfo() + "}";
    }
}
