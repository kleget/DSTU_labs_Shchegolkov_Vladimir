package lab6;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;

/**
 * Task 2: reusable Curve class demo with f(x) = sin(x) on [0; 2*pi].
 */
public class Task2CurveDemo extends JFrame {
    public Task2CurveDemo() {
        super("Task 2: Curve class demo");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        Curve curve = new Curve();
        curve.setData(Math::sin, 0, 2 * Math.PI, 400);
        curve.setColor(Color.BLUE);
        add(new CurvePanel(curve));
        pack();
        setLocationRelativeTo(null);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task2CurveDemo().setVisible(true));
    }

    private static class CurvePanel extends JPanel {
        private final Curve curve;

        private CurvePanel(Curve curve) {
            this.curve = curve;
            setPreferredSize(new Dimension(300, 300));
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2 = (Graphics2D) g.create();
            java.awt.Rectangle rect = new java.awt.Rectangle(20, 20, getWidth() - 40, getHeight() - 40);
            curve.draw(g2, rect, curve.getMinX(), curve.getMaxX(), curve.getMinY(), curve.getMaxY());
            g2.dispose();
        }
    }
}
