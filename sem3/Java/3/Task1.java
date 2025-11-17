public class Task1 {
    public static void main(String[] args) {
        double start = Math.PI / 15;
        double end = Math.PI;
        double step = Math.PI / 15;
        
        System.out.println("x\t\t\tsin(x)\t\t\tf(x)");
        System.out.println("------------------------------------------------");
        
        for (double x = start; x <= end; x += step) {
            double sinX = Math.sin(x);
            double fX = Math.exp(x) / (x * Math.log10(x));
            System.out.printf("%10.5f\t\t%15.7e\t\t%15.7e%n", x, sinX, fX);
        }
    }
}