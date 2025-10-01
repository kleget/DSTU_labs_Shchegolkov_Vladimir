public class Task4 {
    public static void main(String[] args) {
        if (args.length != 5) {
            System.out.println("Использование: java Task4 <R> <r> <x> <y>");
            System.out.println("Пример: java Task4 100.0 20.0 15.0 10.0");
            return;
        }
        
        try {
            double R = Double.parseDouble(args[0]);
            double r = Double.parseDouble(args[1]);
            double x = Double.parseDouble(args[2]);
            double y = Double.parseDouble(args[3]);
            
            double distance = Math.sqrt(x * x + y * y);
            String status;
            
            if (distance > R) {
                status = "Не обнаружен";
            } else if (distance > r) {
                status = "Обнаружен";
            } else {
                status = "Тревога";
            }
            
            System.out.printf("R=%.1f, r=%.1f, координаты(%.1f,%.1f)\n", R, r, x, y);
            System.out.printf("Расстояние: %.2f\nСтатус: %s\n", distance, status);
            
        } catch (NumberFormatException e) {
            System.out.println("Ошибка: все аргументы должны быть числами");
        }
    }
}