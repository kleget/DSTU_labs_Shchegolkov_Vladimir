package lab6;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Rectangle;

/**
 * Ось рисует только линию по границе области.
 */
public class Axis {
    private final boolean horizontal;
    private double min;
    private double max;

    public Axis(boolean horizontal, double min, double max) {
        this.horizontal = horizontal;
        this.min = min;
        this.max = max;
    }

    public double getMin() {
        return min;
    }

    public double getMax() {
        return max;
    }

    public void draw(Graphics2D g, Rectangle plotArea) {
        g.setColor(Color.GRAY);
        if (horizontal) {
            int y = plotArea.y + plotArea.height;
            g.drawLine(plotArea.x, y, plotArea.x + plotArea.width, y);
        } else {
            g.drawLine(plotArea.x, plotArea.y, plotArea.x, plotArea.y + plotArea.height);
        }
    }
}
