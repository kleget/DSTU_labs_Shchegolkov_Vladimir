package lab6;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;

/**
 * Task 3: Graph + Axis + Curve example.
 */
public class Task3GraphDemo extends JFrame {
    private final Graph graph;

    public Task3GraphDemo() {
        super("Task 3: Graph system");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        Axis xAxis = new Axis(true, 0, 2 * Math.PI);
        Axis yAxis = new Axis(false, -1.5, 1.5);
        graph = new Graph(xAxis, yAxis);
        Curve sinCurve = new Curve();
        sinCurve.setData(Math::sin, 0, 2 * Math.PI, 400);
        sinCurve.setColor(Color.RED);
        graph.addCurve(sinCurve);
        add(new GraphPanel());
        pack();
        setLocationRelativeTo(null);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task3GraphDemo().setVisible(true));
    }

    private class GraphPanel extends JPanel {
        private GraphPanel() {
            setPreferredSize(new Dimension(400, 320));
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2 = (Graphics2D) g.create();
            graph.draw(g2, new Rectangle(0, 0, getWidth(), getHeight()));
            g2.dispose();
        }
    }
}
