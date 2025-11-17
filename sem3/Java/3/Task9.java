public class Task9 {
    public static void main(String[] args) {
        String federalPattern = "^(\\+7|8)[\\s\\-\\(]?\\d{3}[\\s\\-\\)]?\\d{3}[\\s\\-]?\\d{2}[\\s\\-]?\\d{2}$";
        String municipalPattern = ".*[23][\\s\\-]?\\d{2}[\\s\\-]?\\d{2}[\\s\\-]?\\d{2}.*";
        
        String[] testNumbers = {
            "+79043781661", "+7 904 378 1661", "+7-904-378-16-61",
            "89043781661", "12345678901"
        };
        
        System.out.println("Проверка федеральных номеров:");
        for (String number : testNumbers) {
            System.out.println(number + " : " + (number.matches(federalPattern) ? "верный" : "неверный"));
        }
        
        String testString = "Мои номера 220-30-40 и 8904-378-16-61 не считая служебных";
        System.out.println("\nСодержит муниципальный номер: " + testString.matches(municipalPattern));
    }
}