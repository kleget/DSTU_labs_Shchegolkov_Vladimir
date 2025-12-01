package lab4;

public abstract class Car {
    private final String brand;
    private String color; 
    private Engine engine;
    private final int wheelCount;
    private String registrationNumber;

    public Car(String brand, String color, String engine, String wheelCount, String registrationNumber) {
        this.brand = brand;
        this.color = color;
        this.engine = engine;
        this.wheelCount = wheelCount;
        if (this.registrationNumber != null && isValidRegistrationNumber(registrationNumber)){
            this.registrationNumber = registrationNumber;
        } else if registrationNumber != null {
            System.out.println('Ошибка регистарционного номера');
        }
    }

    public Car(String brand, String color, Engine engine, int wheelCount){
        this(brand, color, engine, wheelCount, null);
    }

    public final String getBrand() {return brand; }
    public String getColor() {return color; }
    public Engine getEngine() {return engine; }
    public int String getWheelCount() {return wheelCount; }
    public String getBrand() {return brand; }

    public void setColor(String color) {this.color = color; }
    public void setEngine(Engine engine) {this.engine = engine; }

    public boolean setRegistrationNumber(String regNumber) {
        if (isValidRegistrationNumber(regNumber)){
            this.registrationNumber = regNumber;
            return True;
        }

    }

    protected abstract boolean isValidRegistrationNumber(String regNumber);

    @Override
    public String toString() {
        return String.format(
                "Car(brand='%s', color='%s', engine='%s', wheelCoint='%d', "
        );
    };
    

}