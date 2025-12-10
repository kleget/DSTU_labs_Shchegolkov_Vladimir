package lab6;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.util.function.DoubleUnaryOperator;

/**
 * Минимальная реализация кривой: храним табличку и умеем рисовать линии.
 */
public class Curve {
    private double[] xs = new double[0];
    private double[] ys = new double[0];
    private double minX;
    private double maxX;
    private double minY;
    private double maxY;
    private Color color = Color.RED;

    public void setColor(Color color) {
        this.color = color;
    }

    public void setData(DoubleUnaryOperator function, double from, double to, int points) {
        if (points < 2) {
            points = 2;
        }
        xs = new double[points];
        ys = new double[points];
        double step = (to - from) / (points - 1);
        minX = from;
        maxX = to;
        minY = Double.MAX_VALUE;
        maxY = -Double.MAX_VALUE;
        for (int i = 0; i < points; i++) {
            double x = from + i * step;
            double y = function.applyAsDouble(x);
            xs[i] = x;
            ys[i] = y;
            minY = Math.min(minY, y);
            maxY = Math.max(maxY, y);
        }
        if (minY == maxY) {
            minY -= 1;
            maxY += 1;
        }
    }

    public void setData(double[] xs, double[] ys) {
        if (xs == null || ys == null || xs.length != ys.length || xs.length == 0) {
            throw new IllegalArgumentException("Точки заданы неверно");
        }
        this.xs = xs.clone();
        this.ys = ys.clone();
        minX = xs[0];
        maxX = xs[0];
        minY = ys[0];
        maxY = ys[0];
        for (int i = 1; i < xs.length; i++) {
            minX = Math.min(minX, xs[i]);
            maxX = Math.max(maxX, xs[i]);
            minY = Math.min(minY, ys[i]);
            maxY = Math.max(maxY, ys[i]);
        }
        if (minY == maxY) {
            minY -= 1;
            maxY += 1;
        }
    }

    public double getMinX() {
        return minX;
    }

    public double getMaxX() {
        return maxX;
    }

    public double getMinY() {
        return minY;
    }

    public double getMaxY() {
        return maxY;
    }

    public void draw(Graphics2D g, Rectangle area, double minX, double maxX, double minY, double maxY) {
        if (xs.length < 2) {
            return;
        }
        g.setColor(color);
        for (int i = 0; i < xs.length - 1; i++) {
            int x1 = scale(xs[i], minX, maxX, area.x, area.x + area.width);
            int y1 = scale(ys[i], minY, maxY, area.y + area.height, area.y);
            int x2 = scale(xs[i + 1], minX, maxX, area.x, area.x + area.width);
            int y2 = scale(ys[i + 1], minY, maxY, area.y + area.height, area.y);
            g.drawLine(x1, y1, x2, y2);
        }
    }

    private int scale(double value, double srcMin, double srcMax, double dstMin, double dstMax) {
        double ratio = (value - srcMin) / (srcMax - srcMin);
        return (int) Math.round(dstMin + ratio * (dstMax - dstMin));
    }
}
