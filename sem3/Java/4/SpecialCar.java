// File: lab4/SpecialCar.java
package lab4;

public class SpecialCar extends Car {
    public SpecialCar(String brand, String color, Engine engine, String registrationNumber) {
        super(brand, color, engine, 4, registrationNumber);
    }

    public SpecialCar(String brand, String color, Engine engine) {
        this(brand, color, engine, null);
    }

    // Пример: специальный формат - XX 0000 00 RUS
    @Override
    protected boolean isValidRegistrationNumber(String regNumber) {
        if (regNumber == null) return false;
        String regex = "[ABEKMHOPCTYX]{2}\\s\\d{4}\\s\\d{2}\\sRUS";
        return regNumber.matches(regex);
    }

    @Override
    public String toString() {
        return "SpecialCar{" + super.toString().substring(4);
    }
}