public class Task3 {
    public static void main(String[] args) {
        // Заданные параметры
        double R = 100.0;  // максимальная дальность обнаружения
        double r = 20.0;   // радиус тревоги
        
        // Координаты предмета
        double x = 15.0;
        double y = 10.0;
        
        // Расчет расстояния до объекта
        double distance = Math.sqrt(x * x + y * y);
        
        // Определение статуса
        String status;
        if (distance > R) {
            status = "Не обнаружен";
        } else if (distance > r) {
            status = "Обнаружен";
        } else {
            status = "Тревога";
        }
        
        System.out.printf("Расстояние: %.2f\nСтатус: %s\n", distance, status);
    }
}