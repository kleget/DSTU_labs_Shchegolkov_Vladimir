package lab6.lab_gui.graph;

import javax.swing.*;
import java.awt.*;

public class GraphPanel {
    private Curve curve;
    private Axis axisX;
    private Axis axisY;
    private Rectangle wordRect;

    public GraphPanel(Curve curve, Axis axisX, Axis axisY, Rectangle wordRect) {
        this.curve = curve;
        this.axisX = axisX;
        this.axisY = axisY;
        this.wordRect = wordRect;
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        Rectangle screenRect = new Rectangle(0, 0, getWidth(), getHeight());
        axisX.drawX(g2, screenRect, screenRect);
        axisY.drawY(g2, screenRect, screenRect);

        curve.draw(g2, screenRect, screenRect);
    }
}
