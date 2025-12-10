package lab6;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

/**
 * Максимально простая панель: щёлкнул — увидел координаты, буквой сменил цвет.
 */
public class Task4MouseCoordinates extends JFrame {
    public Task4MouseCoordinates() {
        super("Task 4");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        add(new CoordinatesPanel());
        pack();
        setLocationRelativeTo(null);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task4MouseCoordinates().setVisible(true));
    }

    private static class CoordinatesPanel extends JPanel {
        private Point point;
        private Color color = Color.BLACK;

        private CoordinatesPanel() {
            setPreferredSize(new Dimension(400, 300));
            setBackground(Color.WHITE);
            addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    point = e.getPoint();
                    repaint();
                }
            });
            addKeyListener(new KeyAdapter() {
                @Override
                public void keyTyped(KeyEvent e) {
                    switch (Character.toLowerCase(e.getKeyChar())) {
                        case 'b' -> color = Color.BLACK;
                        case 'w' -> color = Color.WHITE;
                        case 'r' -> color = Color.RED;
                        case 'g' -> color = Color.GREEN;
                        case 'o' -> color = Color.ORANGE;
                        default -> {
                            return;
                        }
                    }
                    repaint();
                }
            });
            setFocusable(true);
        }

        @Override
        public void addNotify() {
            super.addNotify();
            requestFocusInWindow();
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            if (point != null) {
                g.setColor(color.equals(Color.WHITE) ? Color.BLACK : color);
                g.drawString(point.x + ", " + point.y, point.x + 5, point.y - 5);
                g.drawOval(point.x - 3, point.y - 3, 6, 6);
            }
        }
    }
}
