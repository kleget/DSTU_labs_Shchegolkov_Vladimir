// File: lab4/Main.java
package lab4;

import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        // Тестирование Задания 1-4 (Car, Engine)
        System.out.println("--- Тест Car ---");
        Engine engine1 = new Engine("ENG123", 150.0, 2.0, 8.5, "Petrol", 4);
        // Car теперь абстрактный, создаем Sedan
        Sedan car1 = new Sedan("Toyota", "Red", engine1, "A 123 BC 123 RUS");
        System.out.println(car1);
        car1.setColor("Blue");
        System.out.println("После смены цвета: " + car1);

        // Тестирование Задания 2 (Complex)
        System.out.println("\n--- Тест Complex ---");
        Complex c1 = new Complex(3, 4);
        Complex c2 = new Complex(1, -2);
        System.out.println("c1 = " + c1.toAlgebraicForm());
        System.out.println("c2 = " + c2.toAlgebraicForm());
        System.out.println("c1 + c2 = " + c1.add(c2));
        System.out.println("c1 * c2 = " + c1.multiply(c2));

        // Тестирование Задания 3 (ComplexMath)
        System.out.println("\n--- Тест ComplexMath ---");
        System.out.println("exp(c1) = " + ComplexMath.exp(c1));
        System.out.println("sin(c1) = " + ComplexMath.sin(c1));
        System.out.println("cosh(c1) = " + ComplexMath.cosh(c1));

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

        // Тестирование Задания 9 (Plot)
        System.out.println("\n--- Тест Plot ---");
        Plot plot = new Plot("Примерный график", 800, 600);
        Curve curve = new Curve(Arrays.asList(new Point(0, 0), new Point(1, 1), new Point(2, 4)), "Red", "y=x^2");
        Axis xAxis = new Axis("X", "Время (с)");
        Axis yAxis = new Axis("Y", "Значение");
        Grid grid = new Grid("LightGray", "Dashed");
        Caption caption = new Caption("Квадратичная функция", new Point(1, 2));

        plot.addCurve(curve);
        plot.addAxis(xAxis);
        plot.addAxis(yAxis);
        plot.addGrid(grid);
        plot.addCaption(caption);

        plot.draw();
    }
}