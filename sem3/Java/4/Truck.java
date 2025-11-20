// File: lab4/Truck.java
package lab4;

public class Truck extends Car {
    public Truck(String brand, String color, Engine engine, String registrationNumber) {
        super(brand, color, engine, 6, registrationNumber); // Пример: грузовик с 6 колесами
    }

    public Truck(String brand, String color, Engine engine) {
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
        return "Truck{" + super.toString().substring(4) + "}";
    }
}