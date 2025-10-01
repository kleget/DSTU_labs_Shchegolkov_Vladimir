public class Task10 {
    public static void main(String[] args) {
        String text = "abcd";
        
        System.out.println("Циклические перестановки строки \"" + text + "\":");
        
        for (int i = 0; i < text.length(); i++) {
            String permutation = text.substring(i) + text.substring(0, i);
            System.out.println(permutation);
        }
    }
}