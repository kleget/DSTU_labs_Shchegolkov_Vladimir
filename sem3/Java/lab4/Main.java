package lab4;

public class Main {
    public static void main(String[] args) {
        System.out.println("--- Cars and engines ---");
        Engine petrol20 = new Engine("ENG-001", 150.0, 2.0, 8.2, "Petrol", 4);
        Engine diesel40 = new Engine("ENG-777", 320.0, 4.0, 18.0, "Diesel", 6);

        Sedan sedan = new Sedan("Toyota", "Red", petrol20, "A 123 BC 99 RUS");
        Truck truck = new Truck("Volvo", "Blue", diesel40, "M 456 OP 197 RUS");
        Bus bus = new Bus("Mercedes", "Yellow", diesel40);
        bus.setRegistrationNumber("K 001 AA 50 RUS");
        SpecialCar firetruck = new SpecialCar("Magirus", "White", diesel40, "FT-9001");

        System.out.println(sedan);
        System.out.println(truck);
        System.out.println(bus);
        System.out.println(firetruck);

        System.out.println("\n--- Garage operations ---");
        Garage garage = new Garage(5);
        garage.addCar(sedan);
        garage.addCar(truck);
        garage.addCar(bus);
        garage.addCar(firetruck);
        garage.displayCarsAtBase();
        garage.sendToMission(truck);
        garage.sendToRepair(firetruck);
        garage.displayCarsInMission();
        garage.displayCarsInRepair();
        garage.returnFromMission(truck);
        garage.returnFromRepair(firetruck);
        garage.displayCarsAtBase();

        System.out.println("\n--- Complex numbers ---");
        Complex z1 = new Complex(2, 3);
        Complex z2 = new Complex(1, -1);
        System.out.println("z1 = " + z1);
        System.out.println("z2 = " + z2);
        System.out.println("z1 + z2 = " + z1.add(z2));
        System.out.println("z1 - z2 = " + z1.subtract(z2));
        System.out.println("z1 * z2 = " + z1.multiply(z2));
        System.out.println("z1 / z2 = " + z1.divide(z2));
        System.out.println("conj(z1) = " + z1.conjugate());
        System.out.println("z1 trig form = " + z1.toTrigonometricString());

        System.out.println("\n--- Complex elementary functions ---");
        System.out.println("exp(z1) = " + ComplexMath.exp(z1));
        System.out.println("sin(z1) = " + ComplexMath.sin(z1));
        System.out.println("cos(z1) = " + ComplexMath.cos(z1));
        System.out.println("tan(z1) = " + ComplexMath.tan(z1));
        System.out.println("atan(z2) = " + ComplexMath.atan(z2));
        System.out.println("sinh(z1) = " + ComplexMath.sinh(z1));
        System.out.println("cosh(z1) = " + ComplexMath.cosh(z1));
        System.out.println("tanh(z1) = " + ComplexMath.tanh(z1));
        System.out.println("coth(z1) = " + ComplexMath.coth(z1));

        System.out.println("\n--- Plot description (text instead of graphics) ---");
        Axis xAxis = new Axis("x", -5, 5, 1);
        Axis yAxis = new Axis("y", -3, 3, 1);
        Grid grid = new Grid(0.5, 0.5);
        GraphPlot plot = new GraphPlot("Sine and Cosine", xAxis, yAxis, grid);
        double[] xs = {-Math.PI, -Math.PI / 2, 0, Math.PI / 2, Math.PI};
        double[] sinValues = new double[xs.length];
        double[] cosValues = new double[xs.length];
        for (int i = 0; i < xs.length; i++) {
            sinValues[i] = Math.sin(xs[i]);
            cosValues[i] = Math.cos(xs[i]);
        }
        plot.addCurve(new Curve("sin(x)", "sin", xs, sinValues));
        plot.addCurve(new Curve("cos(x)", "cos", xs, cosValues));
        plot.addNote("Axes drawn through origin, grid every 0.5 units.");
        plot.renderText();
    }
}
