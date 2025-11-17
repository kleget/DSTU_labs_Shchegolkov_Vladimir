import java.util.Scanner;

enum CircleRelation {
    COINCIDENT, TANGENT, INTERSECTING, SEPARATE, FIRST_CONTAINS_SECOND, SECOND_CONTAINS_FIRST
}

public class Task5 {
    public static CircleRelation analyzeCircles(double x1, double y1, double r1,
                                               double x2, double y2, double r2) {
        double distance = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
        double sumRadii = r1 + r2;
        double diffRadii = Math.abs(r1 - r2);
        
        if (distance == 0 && r1 == r2) return CircleRelation.COINCIDENT;
        if (distance == sumRadii || distance == diffRadii) return CircleRelation.TANGENT;
        if (distance < sumRadii && distance > diffRadii) return CircleRelation.INTERSECTING;
        if (distance > sumRadii) return CircleRelation.SEPARATE;
        if (distance < diffRadii) return (r1 > r2) ? CircleRelation.FIRST_CONTAINS_SECOND 
                                                   : CircleRelation.SECOND_CONTAINS_FIRST;
        return CircleRelation.SEPARATE;
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
        
        CircleRelation result = analyzeCircles(x1, y1, r1, x2, y2, r2);
        System.out.println("Результат: " + result);
        
        scanner.close();
    }
}