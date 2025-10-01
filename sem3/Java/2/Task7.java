public class Task7 {
    public static void main(String[] args) {
        String text = "Hello World 123! Привет 456 €";
        
        int letters = 0, lowercase = 0, uppercase = 0;
        int digits = 0, arabicDigits = 0, nonArabicDigits = 0;
        int other = 0, total = text.length();
        
        for (char c : text.toCharArray()) {
            if (Character.isLetter(c)) {
                letters++;
                if (Character.isLowerCase(c)) lowercase++;
                if (Character.isUpperCase(c)) uppercase++;
            } else if (Character.isDigit(c)) {
                digits++;
                // Простая проверка на арабские цифры (0-9)
                if (c >= '0' && c <= '9') arabicDigits++;
                else nonArabicDigits++;
            } else {
                other++;
            }
        }
        
        System.out.println("Анализ строки: \"" + text + "\"");
        System.out.println("Буквы: " + letters + " (строчные: " + lowercase + ", прописные: " + uppercase + ")");
        System.out.println("Цифры: " + digits + " (арабские: " + arabicDigits + ", не арабские: " + nonArabicDigits + ")");
        System.out.println("Прочие символы: " + other);
        System.out.println("Всего символов: " + total);
    }
}