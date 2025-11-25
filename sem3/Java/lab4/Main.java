// File: lab4/Main.java
package lab4;

// import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        // Тестирование Задания 1, 4 (Car, Engine)
        System.out.println("--- Тест Car ---");
        Engine engine1 = new Engine("ENG123", 150.0, 2.0, 8.5, "Petrol", 4);
        // Car теперь абстрактный, создаем Sedan
        Sedan car1 = new Sedan("Toyota", "Red", engine1, "A 123 BC 123 RUS");
        System.out.println(car1);
        car1.setColor("Blue");
        System.out.println("После смены цвета: " + car1);

        // Тестирование Задания 5-6 (Иерархия Car)
        System.out.println("\n--- Тест Иерархии Car ---");
        Sedan sedan = new Sedan("Honda", "White", engine1);
        Bus bus = new Bus("Mercedes", "Yellow", engine1);
        System.out.println(sedan);
        System.out.println(bus);
        sedan.setRegistrationNumber("B 456 DE 78 RUS");
        System.out.println("Седан с новым номером: " + sedan);

        // Тестирование Задания 7 (Garage)
        System.out.println("\n--- Тест Garage ---");
        Garage garage = new Garage(5);
        garage.addCar(sedan);
        garage.addCar(bus);
        garage.displayCarsAtBase();
        garage.sendToMission(sedan);
        garage.displayCarsInMission();
        garage.returnFromMission(sedan);
        garage.displayCarsAtBase();

    }
}