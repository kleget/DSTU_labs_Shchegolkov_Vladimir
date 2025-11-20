// File: lab4/Car.java
package lab4;

public abstract class Car { // abstract - нельзя создать new Car()
    private String registrationNumber; // Регистрационный номер - может меняться
    private final String brand; // Марка - неизменяема (final)
    private String color; // Цвет - может меняться
    private Engine engine; // Объект двигателя - может меняться (заменить двигатель)
    private final int wheelCount; // Кол-во колес - неизменяемо (final)

    // Конструктор
    public Car(String brand, String color, Engine engine, int wheelCount, String registrationNumber) {
        this.brand = brand;
        this.color = color;
        this.engine = engine;
        this.wheelCount = wheelCount;
        // Проверка и установка регистрационного номера
        if (registrationNumber != null && isValidRegistrationNumber(regNumber)) { // regNumber - опечатка? Должно быть registrationNumber
            this.registrationNumber = registrationNumber;
        } else if (registrationNumber != null) {
            System.out.println("Предупреждение: Неверный формат регистрационного номера. Поле оставлено пустым.");
        }
    }

    // Перегруженный конструктор без номера
    public Car(String brand, String color, Engine engine, int wheelCount) {
        this(brand, color, engine, wheelCount, null); // Вызов основного конструктора
    }

    // Геттеры
    public String getRegistrationNumber() { return registrationNumber; }
    public final String getBrand() { return brand; } // final - нельзя переопределить в наследниках
    public String getColor() { return color; }
    public Engine getEngine() { return engine; }
    public int getWheelCount() { return wheelCount; }

    // Сеттеры (для изменяемых)
    public void setColor(String color) { this.color = color; }
    public void setEngine(Engine engine) { this.engine = engine; }

    // Метод для установки регистрационного номера
    public boolean setRegistrationNumber(String regNumber) {
        if (isValidRegistrationNumber(regNumber)) {
            this.registrationNumber = regNumber;
            return true; // Успешно установлен
        }
        return false; // Неверный формат
    }

    // Абстрактный метод - должен быть реализован в наследниках
    protected abstract boolean isValidRegistrationNumber(String regNumber);

    @Override
    public String toString() {
        return String.format(
            "Car{registrationNumber='%s', brand='%s', color='%s', engine=%s, wheelCount=%d}",
            registrationNumber, brand, color, engine, wheelCount
        );
    }
}