import java.util.Scanner;

public class Task4 {
    public static int analyzeCircles(double x1, double y1, double r1, 
                                   double x2, double y2, double r2) {
        double distance = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
        double sumRadii = r1 + r2;
        double diffRadii = Math.abs(r1 - r2);
        
        if (distance == 0 && r1 == r2) return 0;
        if (distance == sumRadii || distance == diffRadii) return 1;
        if (distance < sumRadii && distance > diffRadii) return 2;
        if (distance > sumRadii) return 3;
        if (distance < diffRadii) return (r1 > r2) ? 4 : 5;
        
        return -1;
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Введите параметры первой окружности:");
        double x1 = scanner.nextDouble();
        double y1 = scanner.nextDouble();
        double r1 = scanner.nextDouble();
        
        System.out.println("Введите параметры второй окружности:");
        double x2 = scanner.nextDouble();
        double y2 = scanner.nextDouble();
        double r2 = scanner.nextDouble();
        
        int result = analyzeCircles(x1, y1, r1, x2, y2, r2);
        
        String[] messages = {
            "Окружности совпадают",
            "Окружности касаются", 
            "Окружности пересекаются в двух точках",
            "Окружности не пересекаются",
            "Вторая окружность вложена в первую",
            "Первая окружность вложена во вторую"
        };
        
        System.out.println(messages[result]);
        scanner.close();
    }
}