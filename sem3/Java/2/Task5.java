public class Task5 {
    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Использование: java Task5 <число>");
            return;
        }
        
        try {
            int number = Integer.parseInt(args[0]);
            
            System.out.println("Десятичное: " + number);
            System.out.println("Двоичное: " + Integer.toBinaryString(number));
            System.out.println("Восьмеричное: " + Integer.toOctalString(number));
            System.out.println("Шестнадцатеричное: " + Integer.toHexString(number));
            
        } catch (NumberFormatException e) {
            System.out.println("Ошибка: аргумент должен быть целым числом");
        }
    }
}