import java.util.Scanner;

public class Task6 {
    
    public static double integrateLeftRectangles(double[] x, double[] y) {
        double integral = 0;
        for (int i = 0; i < x.length - 1; i++) {
            integral += y[i] * (x[i + 1] - x[i]);
        }
        return integral;
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Введите начало интервала: ");
        double start = scanner.nextDouble();
        System.out.print("Введите конец интервала: ");
        double end = scanner.nextDouble();
        
        int points = 101;
        double step = (end - start) / (points - 1);
        
        double[] x = new double[points];
        double[] y = new double[points];
        
        for (int i = 0; i < points; i++) {
            x[i] = start + i * step;
            y[i] = Math.exp(x[i]) - Math.pow(x[i], 3);
        }
        
        double numerical = integrateLeftRectangles(x, y);
        double exact = Math.exp(end) - Math.pow(end, 4)/4 - (Math.exp(start) - Math.pow(start, 4)/4);
        
        System.out.printf("Численное значение: %.6f%n", numerical);
        System.out.printf("Точное значение: %.6f%n", exact);
        System.out.printf("Погрешность: %.6f%n", Math.abs(numerical - exact));
        
        scanner.close();
    }
}