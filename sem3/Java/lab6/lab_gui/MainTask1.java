package lab6.lab_gui;



import javax.swing.*;
import java.awt.*;


import static java.lang.Math.*;

public class MainTask1 {

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Задание 1: sin(x)");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

            frame.setSize(300, 300);
            frame.setLocationRelativeTo(null);

            frame.add(new SinPanel());
            frame.setVisible(true);
        });
    }

    static class SinPanel extends JPanel {
        private final double xMin = -PI;
        private final double xMax =  PI;
        private final double yMin = -1.0;
        private final double yMax =  1.0;

        private final int padding = 20;

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2 = (Graphics2D) g;

            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

            int w = getWidth(); // получакм ширину панели
            int h = getHeight();

            // 1) рисуем оси
            g2.setColor(Color.LIGHT_GRAY);
            int x0 = worldToScreenX(0.0, w);
            int y0 = worldToScreenY(0.0, h);

            // ось X
            g2.drawLine(padding, y0, w - padding, y0);
            // ось Y
            g2.drawLine(x0, padding, x0, h - padding);

            // 2) рисуем график sin(x)
            g2.setColor(Color.BLUE);

            int prevX = -1, prevY = -1;
            int nPoints = w; // количество точек ~ числу пикселей по ширине

            for (int i = 0; i < nPoints; i++) {
                double x = xMin + (xMax - xMin) * i / (nPoints - 1);
                double y = sin(x);

                // перевод в экранные координаты
                int sx = worldToScreenX(x, w);
                int sy = worldToScreenY(y, h);

                if (i > 0) { // если это не первая точка, то рисуем отрезок между предыдущей точкой и текущей
                    g2.drawLine(prevX, prevY, sx, sy);
                }

                prevX = sx;
                prevY = sy;
            }
        }

        // Переход от "математического" x к координате на экране
        private int worldToScreenX(double x, int width) {
            double scaleX = (width - 2.0 * padding) / (xMax - xMin);
            return (int) Math.round(padding + (x - xMin) * scaleX);
        }

        // Переход от "математического" y к координате на экране
        private int worldToScreenY(double y, int height) {
            double scaleY = (height - 2.0 * padding) / (yMax - yMin);
            // инвертируем ось Y (внизу – большие значения)
            return (int) Math.round(height - padding - (y - yMin) * scaleY);
        }
    }
}
