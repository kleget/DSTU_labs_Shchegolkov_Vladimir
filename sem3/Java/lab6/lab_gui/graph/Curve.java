package lab6.lab_gui.graph;

import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.util.function.DoubleUnaryOperator;

public class Curve {
    private double[] x;
    private double[] y;

    public void setData(DoubleUnaryOperator f, double xMin, double xMax, int nPoints) {
        x = new double[nPoints];
        y = new double[nPoints];
        double step = (xMax - xMin) / (nPoints - 1);
        for (int i = 0; i < nPoints; i++) {
            x[i] = xMin+i*step;
            y[i] = f.applyAsDouble(x[i]);
        }
    }
    public void draw(Graphics2D g, Rectangle word, Rectangle screen) {}
}
