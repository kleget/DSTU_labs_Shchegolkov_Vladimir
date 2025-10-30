import java.util.regex.*;

public class Task10 {
    public static void main(String[] args) {
        String text = "Мои номера 220-30-40 и 8904-378-16-61 не считая служебных";
        
        Pattern federalPattern = Pattern.compile("(\\+7|8)[\\s\\-\\(]?\\d{3}[\\s\\-\\)]?\\d{3}[\\s\\-]?\\d{2}[\\s\\-]?\\d{2}");
        Pattern municipalPattern = Pattern.compile("[23][\\s\\-]?\\d{2}[\\s\\-]?\\d{2}[\\s\\-]?\\d{2}");
        
        System.out.println("Федеральные номера:");
        Matcher federalMatcher = federalPattern.matcher(text);
        while (federalMatcher.find()) {
            System.out.println(federalMatcher.group());
        }
        
        System.out.println("Муниципальные номера:");
        Matcher municipalMatcher = municipalPattern.matcher(text);
        while (municipalMatcher.find()) {
            System.out.println(municipalMatcher.group());
        }
    }
}