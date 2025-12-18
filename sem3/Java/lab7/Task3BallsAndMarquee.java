package lab7;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Task3BallsAndMarquee extends JFrame {
    public Task3BallsAndMarquee() {
        super("Шарики и бегущая строка");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(700, 500);
        setLocationRelativeTo(null);

        BallPanel ballPanel = new BallPanel();
        MarqueeLabel marquee = new MarqueeLabel(ballPanel);

        JSpinner maxSpinner = new JSpinner(new SpinnerNumberModel(10, 1, 100, 1));
        JButton startBtn = new JButton("Старт");
        JButton stopBtn = new JButton("Стоп");
        JPanel controls = new JPanel(new FlowLayout(FlowLayout.LEFT));
        controls.add(new JLabel("Макс шариков:"));
        controls.add(maxSpinner);
        controls.add(startBtn);
        controls.add(stopBtn);

        startBtn.addActionListener(e -> ballPanel.start());
        stopBtn.addActionListener(e -> ballPanel.stop());
        maxSpinner.addChangeListener(e -> ballPanel.setMax((Integer) maxSpinner.getValue()));

        add(controls, BorderLayout.NORTH);
        add(ballPanel, BorderLayout.CENTER);
        add(marquee, BorderLayout.SOUTH);
    }

    private static class BallPanel extends JPanel {
        private final List<Ball> balls = new ArrayList<>();
        private final Random random = new Random();
        private final Timer timer;
        private int max = 10;

        BallPanel() {
            setBackground(Color.WHITE);
            addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    if (balls.size() >= max) return;
                    double speed = 1 + random.nextDouble() * 3;
                    double part = speed / Math.sqrt(2);
                    balls.add(new Ball(e.getX(), e.getY(), part, -part));
                }
            });
            timer = new Timer(15, e -> tick());
            timer.start();
        }

        void start() {
            timer.start();
        }

        void stop() {
            timer.stop();
        }

        void setMax(int max) {
            this.max = max;
        }

        int getActive() {
            return balls.size();
        }

        int getMax() {
            return max;
        }

        private void tick() {
            for (Ball ball : balls) {
                ball.x += ball.dx;
                ball.y += ball.dy;
                if (ball.x < Ball.R || ball.x > getWidth() - Ball.R) {
                    ball.dx = -ball.dx;
                }
                if (ball.y < Ball.R || ball.y > getHeight() - Ball.R) {
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
                g.fillOval((int) (ball.x - Ball.R), (int) (ball.y - Ball.R), Ball.R * 2, Ball.R * 2);
            }
        }

        private static class Ball {
            static final int R = 12;
            double x, y, dx, dy;

            Ball(double x, double y, double dx, double dy) {
                this.x = x;
                this.y = y;
                this.dx = dx;
                this.dy = dy;
            }
        }
    }

    private static class MarqueeLabel extends JLabel {
        private int x = 0;

        MarqueeLabel(BallPanel source) {
            super(" ", SwingConstants.LEFT);
            setOpaque(true);
            setBackground(Color.BLACK);
            setForeground(Color.GREEN);
            setPreferredSize(new Dimension(0, 30));
            Timer timer = new Timer(40, e -> {
                setText(" Шариков: " + source.getActive() + " / " + source.getMax() + " ");
                x += 3;
                int width = getWidth();
                if (x > width) {
                    x = -getText().length() * 7;
                }
                repaint();
            });
            timer.start();
        }

        @Override
        protected void paintComponent(Graphics g) {
            g.setColor(getBackground());
            g.fillRect(0, 0, getWidth(), getHeight());
            g.setColor(getForeground());
            g.drawString(getText(), x, getHeight() - 10);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Task3BallsAndMarquee().setVisible(true));
    }
}
