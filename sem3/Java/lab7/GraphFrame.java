package lab7;

import javax.swing.*;
import java.awt.*;
// import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;

public class GraphFrame extends JFrame {
    private final JTextField fromField = new JTextField("-5", 5);
    private final JTextField toField = new JTextField("5", 5);
    private final JTextField stepField = new JTextField("0.1", 5);
    private final JComboBox<String> funcCombo = new JComboBox<>(new String[]{
        "sin(x)", "sin(x*x)+cos(x*x)", "2*sin(x)+cos(2*x)"
    });
    private Color curveColor = Color.RED;
    private final GraphPanel graphPanel = new GraphPanel();

    public GraphFrame() {
        super("График функций (простая версия)");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(700, 500);
        setLocationRelativeTo(null);

        JPanel controls = new JPanel(new FlowLayout(FlowLayout.LEFT));
        controls.add(new JLabel("От:"));
        controls.add(fromField);
        controls.add(new JLabel("До:"));
        controls.add(toField);
        controls.add(new JLabel("Шаг:"));
        controls.add(stepField);
        controls.add(funcCombo);
        JButton colorBtn = new JButton("Цвет");
        JButton drawBtn = new JButton("Рисовать");
        controls.add(colorBtn);
        controls.add(drawBtn);

        colorBtn.addActionListener(e -> {
            Color c = JColorChooser.showDialog(this, "Цвет кривой", curveColor);
            if (c != null) {
                curveColor = c;
            }
        });
        drawBtn.addActionListener(e -> graphPanel.repaint());

        add(controls, BorderLayout.NORTH);
        add(graphPanel, BorderLayout.CENTER);
    }

    private double evaluate(double x) {
        int idx = funcCombo.getSelectedIndex();
        return switch (idx) {
            case 0 -> Math.sin(x);
            case 1 -> Math.sin(x * x) + Math.cos(x * x);
            default -> 2 * Math.sin(x) + Math.cos(2 * x);
        };
    }

    private class GraphPanel extends JPanel {
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            double from, to, step;
            try {
                from = Double.parseDouble(fromField.getText().trim());
                to = Double.parseDouble(toField.getText().trim());
                step = Double.parseDouble(stepField.getText().trim());
            } catch (NumberFormatException ex) {
                return;
            }
            if (step <= 0 || to <= from) return;

            List<Double> xs = new ArrayList<>();
            List<Double> ys = new ArrayList<>();
            for (double x = from; x <= to; x += step) {
                xs.add(x);
                ys.add(evaluate(x));
            }

            double minY = ys.stream().min(Double::compareTo).orElse(0.0);
            double maxY = ys.stream().max(Double::compareTo).orElse(0.0);
            if (maxY == minY) {
                maxY = minY + 1;
            }

            int w = getWidth();
            int h = getHeight();
            g.setColor(Color.LIGHT_GRAY);
            g.drawRect(40, 20, w - 60, h - 60);

            // Axes
            g.setColor(Color.GRAY);
            int y0 = (int) (20 + (h - 60) * (maxY / (maxY - minY)));
            int x0 = 40 + (int) ((w - 60) * (-from) / (to - from));
            g.drawLine(40, y0, w - 20, y0);
            g.drawLine(x0, 20, x0, h - 40);
            g.setColor(Color.DARK_GRAY);
            g.drawString("x", w - 30, y0 - 5);
            g.drawString("y", x0 + 5, 30);

            // simple ticks
            int ticks = 6;
            double dxTick = (to - from) / ticks;
            for (int i = 0; i <= ticks; i++) {
                double xv = from + i * dxTick;
                int px = 40 + (int) ((xv - from) / (to - from) * (w - 60));
                g.drawLine(px, y0 - 3, px, y0 + 3);
                g.drawString(String.format("%.1f", xv), px - 10, y0 + 15);
            }
            double dyTick = (maxY - minY) / ticks;
            for (int i = 0; i <= ticks; i++) {
                double yv = minY + i * dyTick;
                int py = 20 + (int) ((maxY - yv) / (maxY - minY) * (h - 60));
                g.drawLine(x0 - 3, py, x0 + 3, py);
                g.drawString(String.format("%.1f", yv), x0 + 6, py + 4);
            }

            g.setColor(curveColor);
            int prevX = -1, prevY = -1;
            for (int i = 0; i < xs.size(); i++) {
                double x = xs.get(i);
                double y = ys.get(i);
                int px = 40 + (int) ((x - from) / (to - from) * (w - 60));
                int py = 20 + (int) ((maxY - y) / (maxY - minY) * (h - 60));
                if (prevX >= 0) {
                    g.drawLine(prevX, prevY, px, py);
                }
                prevX = px;
                prevY = py;
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new GraphFrame().setVisible(true));
    }
}
