public class Task6 {
    
    public static void printUnicodeTable(int startCode, int rows, int cols) {
        System.out.print("   ");
        for (int j = 0; j < cols; j++) {
            System.out.printf("%x ", j);
        }
        System.out.println();
        
        for (int i = 0; i < rows; i++) {
            System.out.printf("%x ", startCode + i * cols);
            for (int j = 0; j < cols; j++) {
                int code = startCode + i * cols + j;
                System.out.print((char)code + " ");
            }
            System.out.println();
        }
    }
    
    public static void main(String[] args) {
        System.out.println("Кириллица (U+0400 - U+04FF):");
        printUnicodeTable(0x0400, 16, 16);
        
        System.out.println("\nЗнаки денежных единиц (U+20A0 - U+20BF):");
        printUnicodeTable(0x20A0, 2, 16);
    }
}