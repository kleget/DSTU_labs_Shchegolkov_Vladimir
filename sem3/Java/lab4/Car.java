package lab4;

public abstract class Car {
    private String registrationNumber;
    private final String brand; // неизменяема = final
    private String color; 
    private Engine engine;
    private final int wheelCount;

    // Конструктор
    public Car(String brand, String color, Engine engine, int wheelCount, String registrationNumber) {
        this.brand = brand;
        this.color = color;
        this.engine = engine;
        this.wheelCount = wheelCount;
        if (registrationNumber != null && isValidRegistrationNumber(registrationNumber)) {
            this.registrationNumber = registrationNumber;
        } else if (registrationNumber != null) {
            System.out.println("Предупреждение: Неверный формат регистрационного номера. Поле оставлено пустым.");
        }
    }

    // Перегруженный конструктор без номера
    public Car(String brand, String color, Engine engine, int wheelCount) {
        this(brand, color, engine, wheelCount, null); // Вызов основного конструктора
    }

    public String getRegistrationNumber() { return registrationNumber; }
    public final String getBrand() { return brand; }
    public String getColor() { return color; }
    public Engine getEngine() { return engine; }
    public int getWheelCount() { return wheelCount; }

    public void setColor(String color) { this.color = color; }
    public void setEngine(Engine engine) { this.engine = engine; }

    public boolean setRegistrationNumber(String regNumber) {
        if (isValidRegistrationNumber(regNumber)) {
            this.registrationNumber = regNumber;
            return true;
        }
        return false;
    }

    protected abstract boolean isValidRegistrationNumber(String regNumber);

    @Override
    public String toString() {
        return String.format(
            "Car{registrationNumber='%s', brand='%s', color='%s', engine=%s, wheelCount=%d}",
            registrationNumber, brand, color, engine, wheelCount
        );
    }
}