package lab6;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;

/**
 * Task 1: display sin(x) for x in [-PI; PI] inside a 300x300 window.
 */
public class Task1SinePlot extends JFrame {
    public Task1SinePlot() {
        super("Task 1: sin(x)");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        add(new SimpleSinePanel(-Math.PI, Math.PI));
        pack();
        setLocationRelativeTo(null);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task1SinePlot().setVisible(true));
    }

    private static class SimpleSinePanel extends JPanel {
        private final double start;
        private final double end;

        private SimpleSinePanel(double start, double end) {
            this.start = start;
            this.end = end;
            setPreferredSize(new Dimension(300, 300));
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            int width = getWidth();
            int height = getHeight();
            g.setColor(Color.WHITE);
            g.fillRect(0, 0, width, height);
            g.setColor(Color.BLACK);
            g.drawRect(10, 10, width - 20, height - 20);
            int prevX = toScreenX(start, width);
            int prevY = toScreenY(Math.sin(start), height);
            g.setColor(Color.RED);
            int samples = 200;
            for (int i = 1; i <= samples; i++) {
                double x = start + i * (end - start) / samples;
                double y = Math.sin(x);
                int screenX = toScreenX(x, width);
                int screenY = toScreenY(y, height);
                g.drawLine(prevX, prevY, screenX, screenY);
                prevX = screenX;
                prevY = screenY;
            }
        }

        private int toScreenX(double x, int width) {
            double normalized = (x - start) / (end - start);
            return (int) Math.round(10 + normalized * (width - 20));
        }

        private int toScreenY(double y, int height) {
            double normalized = (y + 1) / 2.0;
            return (int) Math.round(10 + (1 - normalized) * (height - 20));
        }
    }
}
