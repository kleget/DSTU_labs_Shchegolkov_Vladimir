// File: lab4/Sedan.java
package lab4;

public class Sedan extends Car {
    public Sedan(String brand, String color, Engine engine, String registrationNumber) {
        super(brand, color, engine, 4, registrationNumber);
    }

    public Sedan(String brand, String color, Engine engine) {
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
        return "Sedan{" + super.toString().substring(4) + "}";
    }
}