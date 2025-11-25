package lab4;

public class Truck extends Car {
    public Truck(String brand, String color, Engine engine, String registrationNumber) {
        super(brand, color, engine, 6, registrationNumber); // Грузовик с 6 колесами
    }

    public Truck(String brand, String color, Engine engine) {
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
        return "Truck{" + super.toString().substring(4) + "}";
    }
}