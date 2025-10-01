public class Task9 {
    public static void main(String[] args) {
        String text = "abracadabra";
        String substring = "abra";
        
        int count = 0;
        int index = 0;
        
        while ((index = text.indexOf(substring, index)) != -1) {
            count++;
            index += substring.length(); // Перемещаемся после найденной подстроки
        }
        
        System.out.println("Строка: \"" + text + "\"");
        System.out.println("Подстрока: \"" + substring + "\"");
        System.out.println("Количество вхождений: " + count);
    }
}