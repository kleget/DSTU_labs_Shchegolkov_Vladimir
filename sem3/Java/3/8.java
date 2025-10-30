import java.util.Scanner;

public class Task8 {
    
    public static double horner(double[] coefficients, double x) {
        double result = coefficients[0];
        for (int i = 1; i < coefficients.length; i++) {
            result = result * x + coefficients[i];
        }
        return result;
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Введите степень полинома: ");
        int degree = scanner.nextInt();
        double[] coefficients = new double[degree + 1];
        
        System.out.println("Введите коэффициенты (от старшего к младшему):");
        for (int i = 0; i <= degree; i++) {
            System.out.printf("a%d: ", degree - i);
            coefficients[i] = scanner.nextDouble();
        }
        
        System.out.print("Введите точку x: ");
        double x = scanner.nextDouble();
        
        double result = horner(coefficients, x);
        System.out.printf("Значение полинома в точке %.1f: %.1f%n", x, result);
        
        scanner.close();
    }
}