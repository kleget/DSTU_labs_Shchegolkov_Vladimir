import java.util.Arrays;
import java.util.Scanner;

public class Task3 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int[][] matrix = new int[3][3];
        
        System.out.println("Введите матрицу 3x3:");
        for (int i = 0; i < 3; i++) {
            System.out.print("Строка " + (i+1) + " (3 числа через пробел): ");
            for (int j = 0; j < 3; j++) {
                matrix[i][j] = scanner.nextInt();
            }
        }
        
        System.out.println("Матрица до сортировки:");
        printMatrix(matrix);
        
        // Сортируем каждую строку
        for (int i = 0; i < matrix.length; i++) {
            Arrays.sort(matrix[i]);
        }
        
        System.out.println("Матрица после сортировки:");
        printMatrix(matrix);
        
        scanner.close();
    }
    
    public static void printMatrix(int[][] matrix) {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println();
        }
    }
}