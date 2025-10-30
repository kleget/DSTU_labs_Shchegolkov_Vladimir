import java.util.Scanner;

public class Task2 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Введите количество строк: ");
        int rows = scanner.nextInt();
        
        int[][] matrix = new int[rows][];
        
        // Ввод рваного массива
        for (int i = 0; i < rows; i++) {
            System.out.print("Введите количество элементов в строке " + (i+1) + ": ");
            int cols = scanner.nextInt();
            matrix[i] = new int[cols];
            
            System.out.print("Введите " + cols + " элементов через пробел: ");
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = scanner.nextInt();
            }
        }
        
        // Поиск наибольшего отрицательного
        int maxNegative = Integer.MIN_VALUE;
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                int element = matrix[i][j];
                if (element < 0 && element > maxNegative) {
                    maxNegative = element;
                }
            }
        }
        
        if (maxNegative != Integer.MIN_VALUE) {
            System.out.println("Наибольший отрицательный элемент: " + maxNegative);
        } else {
            System.out.println("Отрицательных элементов нет");
        }
        
        scanner.close();
    }
}