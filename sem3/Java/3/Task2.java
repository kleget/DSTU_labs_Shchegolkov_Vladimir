import java.util.Scanner;

public class Task2 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Введите количество строк: ");
        int rows = scanner.nextInt();

        System.out.print("Введите количество столбцов: ");
        int cols = scanner.nextInt();
        
        int[][] matrix = new int[rows][cols];


        for (int i=0; i < rows; i++){
            for (int j=0; j < cols; j++){
                System.out.print("Введите числа для строки " + i + " столбца " + j + ": ");
                // int num = scanner.nextInt();
                matrix[i][j] = scanner.nextInt();
            }
        }


        

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