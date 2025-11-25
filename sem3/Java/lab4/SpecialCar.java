package lab4;

public class SpecialCar extends Car {
    public SpecialCar(String brand, String color, Engine engine, String registrationNumber) {
        super(brand, color, engine, 4, registrationNumber);
    }

    public SpecialCar(String brand, String color, Engine engine) {
        this(brand, color, engine, null);
    }

    @Override
    protected boolean isValidRegistrationNumber(String regNumber) {
        if (regNumber == null) return false;
        String regex = "[АВЕКМНОРСТУХ]\\s?\\d{3}\\s?[АВЕКМНОРСТУХ]{2}\\s?\\d{2}\\s?(?:RUS)?";
        return regNumber.matches(regex);
    }

    @Override
    public String toString() {
        return "SpecialCar{" + super.toString().substring(4);
    }
}