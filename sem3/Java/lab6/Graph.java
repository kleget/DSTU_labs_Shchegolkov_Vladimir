package lab6;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.util.ArrayList;
import java.util.List;

/**
 * График хранит оси и список кривых, рисует их по очереди.
 */
public class Graph {
    private final Axis xAxis;
    private final Axis yAxis;
    private final List<Curve> curves = new ArrayList<>();

    public Graph(Axis xAxis, Axis yAxis) {
        this.xAxis = xAxis;
        this.yAxis = yAxis;
    }

    public void addCurve(Curve curve) {
        curves.add(curve);
    }

    public void draw(Graphics2D g, Rectangle area) {
        Rectangle plot = new Rectangle(area.x + 40, area.y + 20, area.width - 60, area.height - 60);
        g.setColor(Color.WHITE);
        g.fillRect(plot.x, plot.y, plot.width, plot.height);
        g.setColor(Color.BLACK);
        g.drawRect(plot.x, plot.y, plot.width, plot.height);
        xAxis.draw(g, plot);
        yAxis.draw(g, plot);
        double minX = xAxis.getMin();
        double maxX = xAxis.getMax();
        double minY = yAxis.getMin();
        double maxY = yAxis.getMax();
        for (Curve curve : curves) {
            curve.draw(g, plot, minX, maxX, minY, maxY);
        }
    }
}
