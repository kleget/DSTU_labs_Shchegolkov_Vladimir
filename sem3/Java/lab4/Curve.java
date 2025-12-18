package lab4;

import java.util.Arrays;

public class Curve {
    private final String name;
    private final String expression;
    private final double[] xValues;
    private final double[] yValues;

    public Curve(String name, String expression, double[] xValues, double[] yValues) {
        if (xValues.length != yValues.length) {
            throw new IllegalArgumentException("x and y arrays must have the same length");
        }
        this.name = name;
        this.expression = expression;
        this.xValues = Arrays.copyOf(xValues, xValues.length);
        this.yValues = Arrays.copyOf(yValues, yValues.length);
    }

    public String describe() {
        StringBuilder builder = new StringBuilder();
        builder.append(String.format("Curve[%s: %s, points=%d]", name, expression, xValues.length));
        int preview = Math.min(3, xValues.length);
        builder.append(" sample=");
        for (int i = 0; i < preview; i++) {
            builder.append(String.format("(%.2f, %.2f)", xValues[i], yValues[i]));
            if (i < preview - 1) {
                builder.append(", ");
            }
        }
        return builder.toString();
    }
}
