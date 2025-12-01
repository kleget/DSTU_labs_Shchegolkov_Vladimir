package lab4;

public final class Bus extends Car { // Задание 6: запретить наследование
    public Bus(String brand, String color, Engine engine, String registrationNumber) {
        super(brand, color, engine, 6, registrationNumber);
    }

    public Bus(String brand, String color, Engine engine) {
        this(brand, color, engine, null);
    }

    @Override
    protected boolean isValidRegistrationNumber(String regNumber) {
        if (regNumber == null) return false;
        String regex = "[ABEKMHOPCTYX]\\s\\d{3}\\s[ABEKMHOPCTYX]{2}\\s(\\d{2}|\\d{3})\\sRUS";
        return regNumber.matches(regex);
    }

    @Override
    public String toString() {
        return "Bus{" + super.toString().substring(4) + "}";
    }
}

