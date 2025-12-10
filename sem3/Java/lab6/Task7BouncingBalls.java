package lab6;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import javax.swing.Timer;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Анимация: кликом создаём шарик, он летит под 45° и отскакивает от стен.
 */
public class Task7BouncingBalls extends JFrame {
    public Task7BouncingBalls() {
        super("Task 7");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        add(new BallPanel());
        setSize(500, 400);
        setLocationRelativeTo(null);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task7BouncingBalls().setVisible(true));
    }

    private static class BallPanel extends JPanel {
        private final List<Ball> balls = new ArrayList<>();
        private final Random random = new Random();
        private static final int R = 12;

        private BallPanel() {
            setBackground(Color.WHITE);
            addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    double speed = 1 + random.nextDouble() * 3;
                    double part = speed / Math.sqrt(2);
                    balls.add(new Ball(e.getX(), e.getY(), part, -part));
                }
            });
            new Timer(15, e -> tick()).start();
        }

        private void tick() {
            for (Ball ball : balls) {
                ball.x += ball.dx;
                ball.y += ball.dy;
                if (ball.x < R || ball.x > getWidth() - R) {
                    ball.dx = -ball.dx;
                }
                if (ball.y < R || ball.y > getHeight() - R) {
                    ball.dy = -ball.dy;
                }
            }
            repaint();
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            g.setColor(Color.RED);
            for (Ball ball : balls) {
                g.fillOval((int) (ball.x - R), (int) (ball.y - R), R * 2, R * 2);
            }
        }

        private static class Ball {
            double x, y, dx, dy;

            Ball(double x, double y, double dx, double dy) {
                this.x = x;
                this.y = y;
                this.dx = dx;
                this.dy = dy;
            }
        }
    }
}
