import java.util.Scanner;

public class Task7 {
    
    public static String convertBase(int number, int base) {
        if (number == 0) return "0";
        
        boolean negative = number < 0;
        number = Math.abs(number);
        StringBuilder result = new StringBuilder();
        
        while (number > 0) {
            result.insert(0, number % base);
            number /= base;
        }
        
        return negative ? "-" + result : result.toString();
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Введите число: ");
        int number = scanner.nextInt();
        System.out.print("Введите основание системы (2-8): ");
        int base = scanner.nextInt();
        
        if (base < 2 || base > 8) {
            System.out.println("Основание должно быть от 2 до 8");
        } else {
            String result = convertBase(number, base);
            System.out.printf("%d в %d-чной системе: %s%n", number, base, result);
        }
        
        scanner.close();
    }
}