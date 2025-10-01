public class Task2 {
    public static void main(String[] args) {
        int[] array = {1, -2, 3, -4, -5, 6, -7, 8, -9, 10, -11, 12, -13, 14, -15, 16, -17, 18, -19, 20};
        
        double product = 1.0;
        int count = 0;
        
        for (int num : array) {
            if (num < 0) {
                product *= Math.abs(num);
                count++;
            }
        }
        
        if (count > 0) {
            double geometricMean = Math.pow(product, 1.0 / count);
            System.out.printf("Среднее геометрическое отрицательных элементов: %.4f\n", geometricMean);
        } else {
            System.out.println("Отрицательных элементов нет");
        }
    }
}