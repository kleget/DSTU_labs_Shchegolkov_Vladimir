package lab4;

public class Grid {
    private final double stepX;
    private final double stepY;

    public Grid(double stepX, double stepY) {
        this.stepX = stepX;
        this.stepY = stepY;
    }

    public String describe() {
        return String.format("Grid[stepX=%.2f, stepY=%.2f]", stepX, stepY);
    }
}
