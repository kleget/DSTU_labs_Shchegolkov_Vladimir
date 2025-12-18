package lab4;

public class Axis {
    private final String label;
    private final double min;
    private final double max;
    private final double tickStep;

    public Axis(String label, double min, double max, double tickStep) {
        if (max <= min) {
            throw new IllegalArgumentException("max must be greater than min");
        }
        this.label = label;
        this.min = min;
        this.max = max;
        this.tickStep = tickStep;
    }

    public String describe() {
        return String.format("Axis[label=%s, range=%.2f..%.2f, tick=%.2f]", label, min, max, tickStep);
    }
}
